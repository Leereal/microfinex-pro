from rest_framework import serializers
from apps import branch_products
from apps.branch_products.models import BranchProduct
from apps.branch_products.serializers import BranchProductSerializer
from apps.branches.models import Branch
from apps.group_product.models import GroupProduct
from apps.group_product.serializers import GroupProductSerializer

from apps.groups.models import Group
from apps.groups.serializers import GroupSerializer
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    branches = serializers.SerializerMethodField()

    def get_groups(self,obj):
        group_products = GroupProduct.objects.filter(product=obj)
        return GroupProductSerializer(group_products, many=True).data
    
    def get_branches(self,obj):
        branch_products = BranchProduct.objects.filter(product=obj)
        return BranchProductSerializer(branch_products, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'name', 'is_active','groups','branches', 'created_at', 'last_modified']
