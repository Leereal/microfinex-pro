from django.contrib import admin
from .models import Charge

class ChargeAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'amount_type', 'charge_type', 'loan_status', 'mode', 'is_active', 'created_at', 'last_modified']
    list_filter = ['amount_type', 'charge_type', 'loan_status', 'mode', 'is_active']
    search_fields = ['name', 'description']

admin.site.register(Charge, ChargeAdmin)
