from django.contrib import admin
from .models import PaymentGateway

class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'is_disbursement', 'is_repayment', 'is_active', 'created_at','last_modified')
    list_filter = ('type', 'is_disbursement', 'is_repayment', 'is_active', 'created_at', 'last_modified')
    search_fields = ('name',)
    readonly_fields = ('created_at','last_modified')

admin.site.register(PaymentGateway, PaymentGatewayAdmin)
