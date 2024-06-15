from django.contrib import admin
from .models import Targets

@admin.register(Targets)
class TargetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'amount', 'month_year', 'is_reached', 'user', 'created_at', 'deleted_at')
    list_filter = ('branch', 'is_reached', 'user', 'month_year', 'created_at', 'deleted_at')
    search_fields = ('branch__name',)
    readonly_fields = ('created_at', 'deleted_at')
