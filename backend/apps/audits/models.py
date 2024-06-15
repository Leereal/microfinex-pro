from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from apps.common.models import TimeStampedModel

class AuditLog(TimeStampedModel):
    # The user who made the change
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)    
    # The name of the model where the change occurred
    model_name = models.CharField(max_length=100)    
    # The ID of the record that was changed
    record_id = models.IntegerField()    
    # The name of the field that was changed
    field_name = models.CharField(max_length=100)    
    # The old value of the field
    old_value = models.TextField(default=None, blank=True, null=True)    
    # The new value of the field
    new_value = models.TextField(default=None, blank=True, null=True)
    # The action that was taken (created, updated, deleted)
    action = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"AuditLog - Model: {self.model_name}, Record ID: {self.record_id}, Field: {self.field_name}"
