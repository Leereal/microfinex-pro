from django.contrib import admin
from .models import LoanStatus


class LoanStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'allow_auto_calculations', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_per_page = 20

admin.site.register(LoanStatus, LoanStatusAdmin)