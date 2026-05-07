from rest_framework import serializers
from .models import Interns

class InternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interns
        fields = ["id", "name", "specialization", "email", "status", "created_at"]
        