from rest_framework import serializers
from .models import Interns, Company


# 1. Serializer cho Company (Dùng cho bài 13 - Nested Serializer)
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address']


# 2. Serializer chính cho Interns
class InternSerializer(serializers.ModelSerializer):
    # Trả về chi tiết công ty thay vì chỉ ID (Bài 13)
    # read_only=True giúp tránh lỗi khi bạn POST dữ liệu mà không gửi kèm object công ty
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Interns
        fields = [
            'id', 'name', 'email', 'specialization',
            'status', 'avatar', 'company'
        ]

    # --- BÀI 14: FIELD-LEVEL VALIDATION ---
    def validate_name(self, value):
        """Kiểm tra logic riêng cho trường name"""
        if len(value) < 2:
            raise serializers.ValidationError("Tên thực tập sinh quá ngắn, ít nhất phải 2 ký tự!")
        if "@" in value:
            raise serializers.ValidationError("Tên không được chứa ký tự @!")
        return value

    # --- BÀI 14 & 19: OBJECT-LEVEL VALIDATION (FIXED) ---
    def validate(self, data):
        """
        Kiểm tra logic tổng thể nhiều trường.
        Sử dụng .get() để tránh lỗi 500 (KeyError) khi dùng phương thức PATCH.
        """
        specialization = data.get('specialization')
        status = data.get('status')

        # Logic: Nếu chuyên ngành là Backend thì bắt buộc phải có trạng thái (status)
        # Lưu ý: Khi PATCH ảnh, specialization có thể không có trong 'data'
        if specialization == 'Backend' and status is None:
            raise serializers.ValidationError(
                {"status": "Thực tập sinh chuyên ngành Backend phải có trạng thái cụ thể!"}
            )

        return data