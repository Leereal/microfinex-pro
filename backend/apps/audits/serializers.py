from rest_framework import serializers
from apps.audits.models import AuditLog
from django.contrib.auth import get_user_model


class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
   
    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user",
            "model_name",
            "record_id",
            "field_name",
            "old_value",
            "new_value",
            "action",
            "created_at",
            "last_modified"
        ]
            
    def get_user(self, instance):
        user = instance.user
        if user:
            return {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
        else:
            return None