import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("Email bắt buộc phải có.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("role", User.Role.ADMIN)
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    class Role(models.TextChoices):
        PATIENT = "patient", _("Bệnh nhân")
        DOCTOR  = "doctor",  _("Bác sĩ")
        ADMIN   = "admin",   _("Quản trị viên")

    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email         = models.EmailField(unique=True)
    full_name     = models.CharField(max_length=120)
    phone         = models.CharField(max_length=20, blank=True)
    role          = models.CharField(max_length=10, choices=Role.choices, default=Role.PATIENT)
    is_active     = models.BooleanField(default=True)
    is_staff      = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    avatar        = models.ImageField(upload_to="avatars/", null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        db_table = "users"
        verbose_name = "User"
        indexes = [
            models.Index(fields=["role"]),
            models.Index(fields=["email", "is_active"]),
        ]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

class Clinic(TimeStampedModel):

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name       = models.CharField(max_length=200)
    address    = models.TextField()
    phone      = models.CharField(max_length=20)
    email      = models.EmailField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    open_time  = models.TimeField()
    close_time = models.TimeField()
    is_active  = models.BooleanField(default=True)
    logo       = models.ImageField(upload_to="clinics/", null=True, blank=True)

    class Meta:
        db_table = "clinics"
        verbose_name = "Clinic"
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name


class Patient(TimeStampedModel):

    class Gender(models.TextChoices):
        MALE    = "M", _("Nam")
        FEMALE  = "F", _("Nữ")
        OTHER   = "O", _("Khác")

    class BloodType(models.TextChoices):
        A_POS  = "A+"; A_NEG  = "A-"
        B_POS  = "B+"; B_NEG  = "B-"
        AB_POS = "AB+"; AB_NEG = "AB-"
        O_POS  = "O+"; O_NEG  = "O-"

    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user             = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    date_of_birth    = models.DateField(null=True, blank=True)
    gender           = models.CharField(max_length=2, choices=Gender.choices, blank=True)
    blood_type       = models.CharField(max_length=3, choices=BloodType.choices, blank=True)
    address          = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    emergency_contact_name  = models.CharField(max_length=120, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    allergies        = models.TextField(blank=True, help_text="Dị ứng đã biết")
    chronic_diseases = models.TextField(blank=True, help_text="Bệnh mãn tính")

    class Meta:
        db_table = "patients"
        verbose_name = "Patient"

    def __str__(self):
        return f"Patient: {self.user.full_name}"

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class Doctor(TimeStampedModel):

    class Specialty(models.TextChoices):
        GENERAL      = "general",     _("Đa khoa")
        CARDIOLOGY   = "cardiology",  _("Tim mạch")
        DERMATOLOGY  = "dermatology", _("Da liễu")
        PEDIATRICS   = "pediatrics",  _("Nhi khoa")
        NEUROLOGY    = "neurology",   _("Thần kinh")
        ORTHOPEDICS  = "orthopedics", _("Cơ xương khớp")
        ENT          = "ent",         _("Tai mũi họng")
        OPHTHALMOLOGY = "ophthalmology", _("Mắt")
        PSYCHIATRY   = "psychiatry",  _("Tâm thần")
        OTHER        = "other",       _("Khác")

    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user             = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    clinic           = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, related_name="doctors")
    specialty        = models.CharField(max_length=20, choices=Specialty.choices, default=Specialty.GENERAL)
    license_number   = models.CharField(max_length=50, unique=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    bio              = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    is_accepting_new = models.BooleanField(default=True, help_text="Có nhận bệnh nhân mới không")

    class Meta:
        db_table = "doctors"
        verbose_name = "Doctor"
        indexes = [
            models.Index(fields=["specialty"]),
            models.Index(fields=["clinic", "is_accepting_new"]),
        ]

    def __str__(self):
        return f"Dr. {self.user.full_name} ({self.get_specialty_display()})"


class WorkSchedule(TimeStampedModel):

    class Weekday(models.IntegerChoices):
        MON = 0, _("Thứ 2")
        TUE = 1, _("Thứ 3")
        WED = 2, _("Thứ 4")
        THU = 3, _("Thứ 5")
        FRI = 4, _("Thứ 6")
        SAT = 5, _("Thứ 7")
        SUN = 6, _("Chủ nhật")

    id                = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor            = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="work_schedules")
    weekday           = models.IntegerField(choices=Weekday.choices)
    start_time        = models.TimeField()
    end_time          = models.TimeField()
    slot_duration_min = models.PositiveSmallIntegerField(default=30, help_text="Thời gian mỗi slot (phút)")
    is_active         = models.BooleanField(default=True)

    class Meta:
        db_table = "work_schedules"
        verbose_name = "Work Schedule"
        unique_together = [("doctor", "weekday", "start_time")]
        indexes = [models.Index(fields=["doctor", "weekday", "is_active"])]

    def __str__(self):
        return f"{self.doctor} · {self.get_weekday_display()} {self.start_time}–{self.end_time}"


class TimeSlot(TimeStampedModel):

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule   = models.ForeignKey(WorkSchedule, on_delete=models.CASCADE, related_name="time_slots")
    slot_date  = models.DateField()
    start_time = models.TimeField()
    end_time   = models.TimeField()
    is_booked  = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = "time_slots"
        verbose_name = "Time Slot"
        unique_together = [("schedule", "slot_date", "start_time")]
        indexes = [
            models.Index(fields=["slot_date", "is_booked"]),
            models.Index(fields=["schedule", "slot_date"]),
        ]

    def __str__(self):
        return f"{self.slot_date} {self.start_time} ({'đã đặt' if self.is_booked else 'trống'})"


class Appointment(TimeStampedModel):
    """Lịch hẹn khám — trung tâm của luồng nghiệp vụ."""

    class Status(models.TextChoices):
        PENDING   = "pending",   _("Chờ xác nhận")
        CONFIRMED = "confirmed", _("Đã xác nhận")
        CANCELLED = "cancelled", _("Đã huỷ")
        COMPLETED = "completed", _("Đã khám xong")
        NO_SHOW   = "no_show",   _("Vắng mặt")

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient      = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor       = models.ForeignKey(Doctor,  on_delete=models.CASCADE, related_name="appointments")
    slot         = models.OneToOneField(TimeSlot, on_delete=models.PROTECT, related_name="appointment")
    status       = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING, db_index=True)
    symptoms     = models.TextField(blank=True, help_text="Triệu chứng bệnh nhân mô tả")
    note         = models.TextField(blank=True, help_text="Ghi chú thêm")
    booked_at    = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancel_reason = models.TextField(blank=True)

    class Meta:
        db_table = "appointments"
        verbose_name = "Appointment"
        indexes = [
            models.Index(fields=["patient", "status"]),
            models.Index(fields=["doctor", "status"]),
            models.Index(fields=["booked_at"]),
        ]

    def __str__(self):
        return f"Apt {self.id.hex[:8]} · {self.patient} → {self.doctor} [{self.status}]"

    def confirm(self):
        self.status = self.Status.CONFIRMED
        self.confirmed_at = timezone.now()
        self.save(update_fields=["status", "confirmed_at", "updated_at"])

    def cancel(self, reason=""):
        self.status = self.Status.CANCELLED
        self.cancelled_at = timezone.now()
        self.cancel_reason = reason
        self.slot.is_booked = False
        self.slot.save(update_fields=["is_booked"])
        self.save(update_fields=["status", "cancelled_at", "cancel_reason", "updated_at"])

class MedicalRecord(TimeStampedModel):

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment    = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="medical_record")
    diagnosis      = models.TextField(help_text="Chẩn đoán")
    treatment_plan = models.TextField(blank=True, help_text="Phác đồ điều trị")
    notes          = models.TextField(blank=True, help_text="Ghi chú thêm của bác sĩ")
    follow_up_date = models.DateField(null=True, blank=True, help_text="Ngày tái khám")
    attachments    = models.JSONField(default=list, help_text="Danh sách URL file đính kèm")

    class Meta:
        db_table = "medical_records"
        verbose_name = "Medical Record"

    def __str__(self):
        return f"Record of {self.appointment}"


class Drug(TimeStampedModel):

    class Category(models.TextChoices):
        ANTIBIOTIC   = "antibiotic",   _("Kháng sinh")
        ANALGESIC    = "analgesic",    _("Giảm đau")
        ANTIVIRAL    = "antiviral",    _("Kháng virus")
        ANTIFUNGAL   = "antifungal",   _("Kháng nấm")
        VITAMIN      = "vitamin",      _("Vitamin")
        SUPPLEMENT   = "supplement",   _("Thực phẩm bổ sung")
        CARDIOVASCULAR = "cardiovascular", _("Tim mạch")
        OTHER        = "other",        _("Khác")

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name         = models.CharField(max_length=200, db_index=True)
    generic_name = models.CharField(max_length=200, blank=True, help_text="Tên hoạt chất")
    category     = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    unit         = models.CharField(max_length=20, default="viên", help_text="Đơn vị: viên, ml, gói …")
    description  = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    is_active    = models.BooleanField(default=True)

    class Meta:
        db_table = "drugs"
        verbose_name = "Drug"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category", "is_active"]),
            GinIndex(
                fields=["name"]
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.unit})"


class Prescription(TimeStampedModel):

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record       = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name="prescriptions")
    doctor       = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name="prescriptions")
    issued_at    = models.DateTimeField(auto_now_add=True)
    valid_until  = models.DateField(null=True, blank=True)
    instructions = models.TextField(blank=True, help_text="Hướng dẫn chung của đơn thuốc")
    is_dispensed = models.BooleanField(default=False, help_text="Đã phát thuốc chưa")

    class Meta:
        db_table = "prescriptions"
        verbose_name = "Prescription"
        indexes = [models.Index(fields=["record", "issued_at"])]

    def __str__(self):
        return f"Rx {self.id.hex[:8]} · {self.doctor} · {self.issued_at.date()}"


class PrescriptionItem(models.Model):

    class Frequency(models.TextChoices):
        ONCE_DAILY   = "1x/ngày",  _("1 lần/ngày")
        TWICE_DAILY  = "2x/ngày",  _("2 lần/ngày")
        THREE_DAILY  = "3x/ngày",  _("3 lần/ngày")
        FOUR_DAILY   = "4x/ngày",  _("4 lần/ngày")
        AS_NEEDED    = "khi cần",  _("Khi cần")

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="items")
    drug         = models.ForeignKey(Drug, on_delete=models.PROTECT, related_name="prescription_items")
    dosage       = models.CharField(max_length=50, help_text="Liều dùng mỗi lần, vd: 500mg")
    quantity     = models.PositiveIntegerField(help_text="Số lượng")
    frequency    = models.CharField(max_length=15, choices=Frequency.choices)
    duration_days = models.PositiveSmallIntegerField(default=7, help_text="Số ngày dùng")
    special_note = models.CharField(max_length=200, blank=True, help_text="Lưu ý riêng")

    class Meta:
        db_table = "prescription_items"
        verbose_name = "Prescription Item"

    def __str__(self):
        return f"{self.drug.name} · {self.dosage} · {self.frequency}"

class Payment(TimeStampedModel):

    class Method(models.TextChoices):
        CASH     = "cash",     _("Tiền mặt")
        TRANSFER = "transfer", _("Chuyển khoản")
        MOMO     = "momo",     _("MoMo")
        VNPAY    = "vnpay",    _("VNPay")
        INSURANCE = "insurance", _("Bảo hiểm y tế")

    class Status(models.TextChoices):
        PENDING  = "pending",  _("Chờ thanh toán")
        PAID     = "paid",     _("Đã thanh toán")
        REFUNDED = "refunded", _("Đã hoàn tiền")
        FAILED   = "failed",   _("Thất bại")

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="payment")
    amount      = models.DecimalField(max_digits=12, decimal_places=0)
    method      = models.CharField(max_length=15, choices=Method.choices, default=Method.CASH)
    status      = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, db_index=True)
    transaction_id = models.CharField(max_length=100, blank=True, help_text="Mã giao dịch từ cổng thanh toán")
    paid_at     = models.DateTimeField(null=True, blank=True)
    note        = models.TextField(blank=True)

    class Meta:
        db_table = "payments"
        verbose_name = "Payment"
        indexes = [models.Index(fields=["status", "paid_at"])]

    def __str__(self):
        return f"Payment {self.amount:,}đ · {self.status}"


class AuditLog(models.Model):

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="audit_logs")
    action     = models.CharField(max_length=50, db_index=True, help_text="CREATE / UPDATE / DELETE / LOGIN …")
    model_name = models.CharField(max_length=60, db_index=True)
    object_id  = models.UUIDField(null=True, blank=True)
    diff       = models.JSONField(default=dict, help_text="Trước và sau khi thay đổi")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "audit_logs"
        verbose_name = "Audit Log"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["model_name", "object_id"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self):
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {self.action} on {self.model_name} by {self.user}"
