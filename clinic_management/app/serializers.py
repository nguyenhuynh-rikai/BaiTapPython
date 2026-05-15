"""
MediFlow — api/serializers.py
==============================
Serializers cho toàn bộ API.

Cấu trúc:
  Auth        : RegisterSerializer, LoginSerializer, ChangePasswordSerializer
  Clinic      : ClinicSerializer
  Doctor      : DoctorListSerializer, DoctorDetailSerializer
  Patient     : PatientSerializer, PatientUpdateSerializer
  Appointment : AppointmentCreateSerializer, AppointmentListSerializer,
                AppointmentDetailSerializer
  Slot        : TimeSlotSerializer, AvailableSlotsQuerySerializer
  Medical     : MedicalRecordSerializer, PrescriptionSerializer,
                PrescriptionItemSerializer
  Drug        : DrugSerializer
  Payment     : PaymentSerializer
"""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class TimestampMixin(serializers.Serializer):
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")

class RegisterSerializer(serializers.ModelSerializer):

    password         = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    role             = serializers.ChoiceField(
        choices=["patient", "doctor"],
        default="patient",
    )

    class Meta:
        model  = User
        fields = ["email", "full_name", "phone", "role", "password", "password_confirm"]

    def validate_email(self, value: str) -> str:
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email này đã được sử dụng.")
        return value

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def validate(self, data: dict) -> dict:
        if data["password"] != data.pop("password_confirm"):
            raise serializers.ValidationError({"password_confirm": "Mật khẩu xác nhận không khớp."})
        return data

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Đăng nhập — trả về JWT access + refresh token."""

    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # Output fields (set sau khi validate)
    access  = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    role    = serializers.CharField(read_only=True)

    def validate(self, data: dict) -> dict:
        from django.contrib.auth import authenticate
        user = authenticate(
            request=self.context.get("request"),
            email=data["email"].lower().strip(),
            password=data["password"],
        )
        if not user:
            raise serializers.ValidationError("Email hoặc mật khẩu không đúng.")
        if not user.is_active:
            raise serializers.ValidationError("Tài khoản đã bị vô hiệu hoá.")

        tokens = RefreshToken.for_user(user)
        return {
            "access":  str(tokens.access_token),
            "refresh": str(tokens),
            "user_id": str(user.id),
            "role":    user.role,
        }


class ChangePasswordSerializer(serializers.Serializer):
    """Đổi mật khẩu — yêu cầu mật khẩu cũ."""

    old_password     = serializers.CharField(write_only=True)
    new_password     = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    def validate_old_password(self, value: str) -> str:
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Mật khẩu hiện tại không đúng.")
        return value

    def validate_new_password(self, value: str) -> str:
        validate_password(value)
        return value

    def validate(self, data: dict) -> dict:
        if data["new_password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Mật khẩu xác nhận không khớp."})
        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError({"new_password": "Mật khẩu mới phải khác mật khẩu cũ."})
        return data

    def save(self, **kwargs) -> User:
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user


class UserMeSerializer(serializers.ModelSerializer):
    """Thông tin user hiện tại (GET /api/me/)."""

    class Meta:
        model  = User
        fields = ["id", "email", "full_name", "phone", "role", "email_verified", "created_at"]
        read_only_fields = ["id", "email", "role", "email_verified", "created_at"]



class ClinicSerializer(TimestampMixin, serializers.ModelSerializer):

    class Meta:
        from .models import Clinic
        model  = Clinic
        fields = [
            "id", "name", "address", "phone", "email",
            "open_time", "close_time", "is_active",
            "latitude", "longitude",
            "created_at", "updated_at",
        ]


class DoctorListSerializer(serializers.ModelSerializer):
    """Dùng cho danh sách — ít field, nhanh hơn."""
    full_name        = serializers.CharField(source="user.full_name")
    email            = serializers.EmailField(source="user.email")
    specialty_label  = serializers.CharField(source="get_specialty_display")
    clinic_name      = serializers.CharField(source="clinic.name", default="")
    avatar           = serializers.ImageField(source="user.avatar", default=None)

    class Meta:
        from .models import Doctor
        model  = Doctor
        fields = [
            "id", "full_name", "email", "specialty", "specialty_label",
            "clinic_name", "experience_years", "consultation_fee",
            "is_accepting_new", "avatar",
        ]


class DoctorDetailSerializer(DoctorListSerializer):
    """Dùng cho trang chi tiết — thêm bio + lịch làm việc."""

    from .models import Doctor
    work_schedules = serializers.SerializerMethodField()
    clinic         = ClinicSerializer(read_only=True)

    class Meta(DoctorListSerializer.Meta):
        fields = DoctorListSerializer.Meta.fields + [
            "bio", "license_number", "clinic", "work_schedules",
        ]

    def get_work_schedules(self, obj) -> list:
        schedules = obj.work_schedules.filter(is_active=True).order_by("weekday")
        return [
            {
                "weekday":          s.weekday,
                "weekday_label":    s.get_weekday_display(),
                "start_time":       s.start_time.strftime("%H:%M"),
                "end_time":         s.end_time.strftime("%H:%M"),
                "slot_duration_min": s.slot_duration_min,
            }
            for s in schedules
        ]

class PatientSerializer(serializers.ModelSerializer):
    """Hồ sơ bệnh nhân — dùng cho GET /api/patients/{id}/."""

    full_name        = serializers.CharField(source="user.full_name", read_only=True)
    email            = serializers.EmailField(source="user.email",    read_only=True)
    phone            = serializers.CharField(source="user.phone",     read_only=True)
    age              = serializers.IntegerField(read_only=True)

    class Meta:
        from .models import Patient
        model  = Patient
        fields = [
            "id", "full_name", "email", "phone",
            "date_of_birth", "age", "gender", "blood_type",
            "address", "insurance_number",
            "allergies", "chronic_diseases",
            "emergency_contact_name", "emergency_contact_phone",
        ]
        read_only_fields = ["id", "full_name", "email", "phone", "age"]


class PatientUpdateSerializer(serializers.ModelSerializer):
    """Cập nhật hồ sơ bệnh nhân — chỉ các field được phép thay đổi."""

    class Meta:
        from .models import Patient
        model  = Patient
        fields = [
            "date_of_birth", "gender", "blood_type",
            "address", "insurance_number",
            "allergies", "chronic_diseases",
            "emergency_contact_name", "emergency_contact_phone",
        ]

    def validate_date_of_birth(self, value: date) -> date:
        if value >= date.today():
            raise serializers.ValidationError("Ngày sinh phải trong quá khứ.")
        if value < date(1900, 1, 1):
            raise serializers.ValidationError("Ngày sinh không hợp lệ.")
        return value

class TimeSlotSerializer(serializers.Serializer):
    """Output slot trống — dùng cho GET /api/slots/available/."""

    slot_id    = serializers.CharField()
    doctor_id  = serializers.CharField()
    doctor_name = serializers.CharField()
    specialty  = serializers.CharField()
    date       = serializers.DateField()
    start_time = serializers.TimeField(format="%H:%M")
    end_time   = serializers.TimeField(format="%H:%M")
    is_booked  = serializers.BooleanField()
    display    = serializers.CharField()


class AvailableSlotsQuerySerializer(serializers.Serializer):
    """Query params cho GET /api/slots/available/."""

    doctor_id = serializers.UUIDField(required=False)
    specialty = serializers.ChoiceField(
        choices=[
            "general", "cardiology", "dermatology", "pediatrics",
            "neurology", "orthopedics", "ent", "ophthalmology",
            "psychiatry", "other",
        ],
        required=False,
    )
    date = serializers.DateField(required=True)

    def validate_date(self, value: date) -> date:
        today    = date.today()
        max_date = today + timedelta(days=60)
        if value < today:
            raise serializers.ValidationError("Không thể xem slot trong quá khứ.")
        if value > max_date:
            raise serializers.ValidationError("Chỉ xem được lịch trong vòng 60 ngày tới.")
        return value

    def validate(self, data: dict) -> dict:
        if not data.get("doctor_id") and not data.get("specialty"):
            raise serializers.ValidationError(
                "Vui lòng cung cấp doctor_id hoặc specialty."
            )
        return data

class AppointmentCreateSerializer(serializers.Serializer):
    """POST /api/appointments/ — đặt lịch hẹn mới."""

    slot_id  = serializers.UUIDField()
    symptoms = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    note     = serializers.CharField(max_length=500,  required=False, allow_blank=True)

    def validate_slot_id(self, value) -> str:
        from .models import TimeSlot
        try:
            slot = TimeSlot.objects.get(pk=value)
        except TimeSlot.DoesNotExist:
            raise serializers.ValidationError("Slot không tồn tại.")
        if slot.is_booked:
            raise serializers.ValidationError("Slot này đã được đặt.")
        if slot.slot_date < date.today():
            raise serializers.ValidationError("Không thể đặt lịch trong quá khứ.")
        return str(value)


class AppointmentListSerializer(serializers.Serializer):
    """GET /api/appointments/ — danh sách ngắn gọn."""

    id               = serializers.CharField()
    patient_name     = serializers.CharField()
    doctor_name      = serializers.CharField()
    specialty        = serializers.CharField()
    clinic_name      = serializers.CharField()
    slot_date        = serializers.CharField()
    start_time       = serializers.CharField()
    end_time         = serializers.CharField()
    status           = serializers.CharField()
    consultation_fee = serializers.CharField()
    booked_at        = serializers.CharField()


class AppointmentDetailSerializer(AppointmentListSerializer):
    """GET /api/appointments/{id}/ — chi tiết đầy đủ."""

    symptoms         = serializers.CharField()
    note             = serializers.CharField()
    confirmed_at     = serializers.CharField(allow_null=True)
    cancelled_at     = serializers.CharField(allow_null=True)
    cancel_reason    = serializers.CharField()
    has_medical_record = serializers.SerializerMethodField()

    def get_has_medical_record(self, obj) -> bool:
        return hasattr(obj, "medical_record")


class AppointmentCancelSerializer(serializers.Serializer):
    """DELETE /api/appointments/{id}/ — yêu cầu lý do huỷ."""

    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)

class PrescriptionItemSerializer(serializers.ModelSerializer):
    drug_name = serializers.CharField(source="drug.name", read_only=True)
    drug_unit = serializers.CharField(source="drug.unit", read_only=True)

    class Meta:
        from .models import PrescriptionItem
        model  = PrescriptionItem
        fields = [
            "id", "drug", "drug_name", "drug_unit",
            "dosage", "quantity", "frequency",
            "duration_days", "special_note",
        ]


class PrescriptionSerializer(serializers.ModelSerializer):
    items       = PrescriptionItemSerializer(many=True, read_only=True)
    doctor_name = serializers.CharField(source="doctor.user.full_name", read_only=True)

    class Meta:
        from .models import Prescription
        model  = Prescription
        fields = [
            "id", "doctor_name", "issued_at", "valid_until",
            "instructions", "is_dispensed", "items",
        ]
        read_only_fields = ["id", "issued_at"]


class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    """POST /api/appointments/{id}/medical-record/ — bác sĩ tạo hồ sơ sau khám."""

    class Meta:
        from .models import MedicalRecord
        model  = MedicalRecord
        fields = [
            "diagnosis", "treatment_plan", "notes", "follow_up_date",
        ]

    def validate_follow_up_date(self, value: date) -> date:
        if value and value <= date.today():
            raise serializers.ValidationError("Ngày tái khám phải trong tương lai.")
        return value


class MedicalRecordSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True, read_only=True)

    class Meta:
        from .models import MedicalRecord
        model  = MedicalRecord
        fields = [
            "id", "diagnosis", "treatment_plan", "notes",
            "follow_up_date", "attachments", "created_at",
            "prescriptions",
        ]
        read_only_fields = ["id", "created_at"]

class DrugSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        from .models import Drug
        model  = Drug
        fields = [
            "id", "name", "generic_name", "category", "category_label",
            "unit", "description", "side_effects", "is_active",
        ]
        read_only_fields = ["id"]


class PaymentSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    method_label = serializers.CharField(source="get_method_display", read_only=True)

    class Meta:
        from .models import Payment
        model  = Payment
        fields = [
            "id", "appointment", "amount",
            "method", "method_label",
            "status", "status_label",
            "transaction_id", "paid_at", "note",
        ]
        read_only_fields = ["id", "paid_at", "status_label", "method_label"]


# ─────────────────────────────────────────────────────────────
# DASHBOARD / ANALYTICS
# ─────────────────────────────────────────────────────────────

class DoctorWorkloadSerializer(serializers.Serializer):
    """GET /api/doctors/{id}/workload/ — thống kê bác sĩ."""

    doctor_id        = serializers.CharField()
    doctor_name      = serializers.CharField()
    total_slots      = serializers.IntegerField()
    booked_slots     = serializers.IntegerField()
    completed        = serializers.IntegerField()
    cancelled        = serializers.IntegerField()
    no_show          = serializers.IntegerField()
    utilization_pct  = serializers.FloatField()


class WorkloadQuerySerializer(serializers.Serializer):
    """Query params cho workload endpoint."""

    from_date = serializers.DateField(required=False)
    to_date   = serializers.DateField(required=False)

    def validate(self, data: dict) -> dict:
        today = date.today()
        data.setdefault("from_date", today.replace(day=1))   # đầu tháng
        data.setdefault("to_date",   today)
        if data["from_date"] > data["to_date"]:
            raise serializers.ValidationError("from_date phải trước to_date.")
        return data
