from rest_framework import serializers
from .models import LoanApplication, RejectionReason

class RejectionReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RejectionReason
        fields = ['id', 'title', 'description', 'user']

class LoanApplicationSerializer(serializers.ModelSerializer):
    # If you want to display the rejection reason's title instead of its id
    rejection_reason_title = serializers.CharField(source='rejection_reason.title', read_only=True)
    
    class Meta:
        model = LoanApplication
        fields = ['id', 'client', 'amount', 'status', 'rejection_reason', 'rejection_reason_title', 'user', 'branch']
        # Optionally, if you want to include user-friendly text for the 'status' field:
        extra_kwargs = {
            'user': {'read_only': True},
            'branch': {'read_only': True},            
        }

    def validate_amount(self, value):
        """
        Check that the loan amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("The amount must be positive.")
        return value

    def validate_client(self, value):
        """
        Check that the client is active.
        """
        if not value.is_active:
            raise serializers.ValidationError("The client must be active.")
        return value
