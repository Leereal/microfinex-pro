from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Finance, Branch

User = get_user_model()

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = [
            'id', 'title', 'description', 'amount', 'received_from', 'paid_to', 
            'receipt_number', 'receipt_screenshot', 'type', 'created_by', 'branch'
        ]
        extra_kwargs = {
            'description': {'allow_blank': True},
            'received_from': {'allow_blank': True},
            'paid_to': {'allow_blank': True},
            'receipt_number': {'allow_blank': True},
            'receipt_screenshot': {'allow_blank': True},
            'created_by': {'read_only': True},
            'branch': {'read_only': True},
        }

    def validate_amount(self, value):
        """
        Check that the amount is greater than zero.
        """
        if value <= 0:
            raise serializers.ValidationError(_("Amount must be greater than zero."))
        return value

    def validate_type(self, value):
        """
        Ensure the type is one of the predefined choices.
        """
        if value not in [choice[0] for choice in Finance.Type.choices]:
            raise serializers.ValidationError(_("Invalid type for finance."))
        return value

    def validate(self, attrs):
        """
        Further validations that depend on combinations of fields can be added here.
        For example, ensuring that 'received_from' or 'paid_to' is filled based on the type.
        """
        if attrs['type'] in ['income', 'investment'] and not attrs.get('received_from'):
            raise serializers.ValidationError({"received_from": _("This field is required for income and investment types.")})
        if attrs['type'] in ['expense', 'withdrawal'] and not attrs.get('paid_to'):
            raise serializers.ValidationError({"paid_to": _("This field is required for expense and withdrawal types.")})
        return attrs
