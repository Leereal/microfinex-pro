from rest_framework import serializers
from .models import Period

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = ['id', 'name', 'duration', 'duration_unit', 'description']
