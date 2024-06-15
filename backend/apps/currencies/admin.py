from django.contrib import admin
from .models import Currency

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'symbol', 'is_active', 'created_at')
    list_filter = ['is_active']
    search_fields = ('name', 'code', 'symbol')
    readonly_fields = ('created_at', 'last_modified', 'deleted_at')

admin.site.register(Currency, CurrencyAdmin)
