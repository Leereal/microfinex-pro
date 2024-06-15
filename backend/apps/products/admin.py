from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'deleted_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'deleted_at')


