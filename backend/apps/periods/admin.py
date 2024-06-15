from django.contrib import admin
from .models import Period

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration', 'duration_unit', 'description', 'created_at', 'deleted_at')
    list_filter = ('created_at', 'deleted_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'deleted_at')
