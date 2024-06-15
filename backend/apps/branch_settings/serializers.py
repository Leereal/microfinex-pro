from rest_framework import serializers
from .models import BranchSettings

class BranchSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchSettings
        fields = [
            'id',
            'branch',
            'loan_approval_required',
            'loan_application_allowed',
            'min_loan_amount',
            'max_loan_amount',
            'default_interest_rate',
        ]
