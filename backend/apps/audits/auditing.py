import json
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.forms.models import model_to_dict

from apps.audits.serializers import AuditLogSerializer
from .models import AuditLog

class AuditableMixin(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_audit_fields(cls):
        # Override this method in your models to specify fields to audit        
        return [field.name for field in cls._meta.fields if field.name != 'id']

@receiver(pre_save)
def pre_save_handler(sender, instance, **kwargs):
    if issubclass(sender, AuditableMixin):
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._old_values = model_to_dict(old_instance)
        except sender.DoesNotExist:
            instance._old_values = None

@receiver(post_save)
def post_save_handler(sender, instance, created, request=None, **kwargs):  
    if issubclass(sender, AuditableMixin):       
        new_values = model_to_dict(instance)
        if created:
            action = 'created'
            old_values = None
        else:
            action = 'updated'
            old_values = instance._old_values
        
        if not created:  # To save including when created, remove this line
            changes = []
            for field_name in instance.get_audit_fields():            
                old_value = instance._old_values.get(field_name) if instance._old_values else None
                new_value = new_values.get(field_name)
                if old_value != new_value:                
                    changes.append((field_name, old_value, new_value))

            if changes:
                for field_name, old_value, new_value in changes:
                    # Create AuditLog instance using serializer
                     # Ensure both old_value and new_value are converted to string
                    old_value_str = str(old_value) if old_value is not None else None
                    new_value_str = str(new_value) if new_value is not None else None
                    serializer = AuditLogSerializer(data={
                        'user': request.user if request and request.user.is_authenticated else None,
                        'action': action,
                        'model_name': sender.__name__,
                        'record_id': instance.pk,
                        'field_name': field_name,
                        'old_value': old_value_str,
                        'new_value': new_value_str
                    })
                    serializer.is_valid(raise_exception=True)
                    serializer.save()


@receiver(pre_delete)
def pre_delete_handler(sender, instance, request=None, **kwargs):
    if issubclass(sender, AuditableMixin):
        instance._old_values = model_to_dict(instance)
        # Create AuditLog instance using serializer
        old_values = {key: str(value) for key, value in model_to_dict(instance).items()}
        old_values = json.dumps(old_values)
        serializer = AuditLogSerializer(data={
            'user': request.user if request and request.user.is_authenticated else None,
            'action': 'deleted',
            'model_name': sender.__name__,
            'record_id': instance.pk,
            'field_name': 'all fields',
            'old_value': old_values,
            'new_value': None
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()