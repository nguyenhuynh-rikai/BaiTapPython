from rest_framework import serializers
from .models import Interns, Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address']

class InternSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Interns
        fields = ['id', 'name', 'specialization', 'company']