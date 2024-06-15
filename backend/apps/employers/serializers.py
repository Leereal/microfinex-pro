from apps.employers.models import Employer
from rest_framework import serializers

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ('id','contact_person', 'email', 'phone', 'name', 'address', 'employment_date', 'job_title', 'created_by', 'is_active')
        
        