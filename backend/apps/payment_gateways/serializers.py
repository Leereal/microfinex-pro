from rest_framework import serializers
from .models import PaymentGateway

class PaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = ['id', 'name', 'description', 'type', 'is_disbursement', 'is_repayment', 'is_active']
