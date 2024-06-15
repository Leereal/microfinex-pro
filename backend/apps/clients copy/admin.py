from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Client, Contact

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1

class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'email', 'status']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ["branch","created_by","is_active", "status", "gender"]
    inlines = [ContactInline]

    def email(self, obj):
        return obj.emails[0] if obj.emails else None
    email.short_description = _('Email')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # # Check if at least one contact is provided
        # if not obj.contacts.exists():
        #     raise ValidationError(_('At least one contact must be provided for the client.'))

admin.site.register(Client, ClientAdmin)
