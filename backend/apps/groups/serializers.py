from rest_framework import serializers

from apps.group_product.serializers import GroupProductSerializer
from .models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    branch_name = serializers.ReadOnlyField(source='branch.name')
    created_by_full_name = serializers.ReadOnlyField(source='created_by.get_full_name')
    group_products = serializers.SerializerMethodField()

    def get_products(self, obj):
        group_products = obj.group_products.all()
        return GroupProductSerializer(group_products, many=True).data

    class Meta:
        model = Group
        fields = [
            'id', 
            'name', 
            'description', 
            'leader', 
            'email', 
            'phone', 
            'is_active', 
            'branch', 
            'branch_name', 
            'created_by', 
            'created_by_full_name',
            'group_products',
            'status',
            'created_at', 
            'last_modified'
        ]
