from django.contrib import admin
from .models import AuditLog

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'model_name', 'record_id', 'field_name', 'old_value', 'new_value','action', 'created_at','last_modified','deleted_at')
    list_filter = ('model_name', 'user', 'created_at','last_modified','deleted_at')
    search_fields = ('model_name', 'user__firstname', 'record_id', 'field_name','user__email')

admin.site.register(AuditLog, AuditLogAdmin)
