from rest_framework import serializers
from .models import Charge, LoanStatus

class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = [
            'id', 'name', 'description', 'amount', 'amount_type', 'charge_type',
            'charge_application', 'loan_status', 'mode', 'is_active',
        ]

    def validate_amount(self, value):
        """
        Ensure the amount is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_name(self, value):
        """
        Ensure the name is unique and not blank.
        """
        if not value.strip():
            raise serializers.ValidationError("Name must not be blank.")
        if Charge.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A charge with this name already exists.")
        return value

    def validate_loan_status(self, value):
        """
        Ensure the loan status exists.
        """
        if not LoanStatus.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid loan status.")
        return value

    def validate(self, data):
        """
        Additional custom validation can go here.
        For example, ensure that the charge type and amount type combinations are valid.
        """
        if data['amount_type'] == 'percentage' and data['amount'] > 100:
            raise serializers.ValidationError({"amount": "Percentage amount cannot exceed 100."})
        return data
