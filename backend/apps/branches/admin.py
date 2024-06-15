from django.contrib import admin
from .models import Branch

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'phone', 'is_active', 'country')
    search_fields = ('name', 'address', 'email', 'phone')

admin.site.register(Branch, BranchAdmin)
