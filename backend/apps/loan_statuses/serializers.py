from rest_framework import serializers
from .models import LoanStatus

class LoanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanStatus
        fields = ['id', 'name', 'description', 'allow_auto_calculations', 'is_active']
        
    def validate_name(self, value):
        """
        Ensure that no two loan statuses have the same name. Skip check if updating.
        """
        if self.instance is None:  # This is an add operation
            if LoanStatus.objects.filter(name=value).exists():
                raise serializers.ValidationError("A loan status with this name already exists.")
        else:  # This is an update operation
            if LoanStatus.objects.filter(name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A loan status with this name already exists.")
        return value
