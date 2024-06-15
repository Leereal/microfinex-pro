from rest_framework import serializers
from .models import LoanTransaction
from apps.currencies.serializers import CurrencySerializer
from apps.payment_gateways.serializers import PaymentGatewaySerializer
from apps.branches.serializers import BranchSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class LoanTransactionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='loan.client.get_full_name', read_only=True)
    currency = serializers.CharField(source='currency.code')
    
    branch = serializers.CharField(source='branch.name', read_only=True)
    payment_gateway = serializers.CharField(source='payment_gateway.name', required=False)
    created_by = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = LoanTransaction
        fields = ['id', 'loan', 'client_name','description', 'transaction_type', 'debit', 'credit', 'currency', 'created_by', 'branch', 'payment_gateway', 'status']
        read_only_fields = ['id', 'status','branch','loan']
        
    def validate(self, data):
        """
        Validate the transaction data.
        """
        debit = data.get('debit')
        credit = data.get('credit')

        if credit is None and debit is None:
            raise serializers.ValidationError({'debit': 'Debit amount is required.', 'credit': 'Credit amount is required.'})
        
        return data
     