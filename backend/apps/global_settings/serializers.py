from rest_framework import serializers
from .models import GlobalSettings

class GlobalSettingsSerializer(serializers.ModelSerializer):
    company_logo_url = serializers.SerializerMethodField('get_company_logo_url')

    class Meta:
        model = GlobalSettings
        fields = [
            'id', 'company_name', 'company_logo', 'company_logo_url', 'contact_email',
            'contact_phone', 'address', 'default_interest_rate', 'min_loan_amount',
            'max_loan_amount', 'loan_approval_required', 'loan_application_allowed',
            'fiscal_year_start', 'fiscal_year_end', 'currency_code', 'timezone',
        ]
        read_only_fields = ['id']

    def get_company_logo_url(self, obj):
        """
        Method to return the full URL of the company logo if it exists.
        """
        if obj.company_logo:
            return self.context['request'].build_absolute_uri(obj.company_logo.url)
        return None
