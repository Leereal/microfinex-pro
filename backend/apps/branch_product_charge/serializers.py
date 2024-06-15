from rest_framework import serializers

from apps.branch_product_charge.models import BranchProductCharge

class BranchProductChargeSerializer(serializers.ModelSerializer):
    #Combine branch and product names to come up with branch_product_name
    branch_product_name = serializers.SerializerMethodField()
    branch_product_charge_name = serializers.SerializerMethodField()

    class Meta:
        model = BranchProductCharge
        fields = ['id','branch_product_name','branch_product_charge_name','branch_product', 'charge', 'is_active']

    def get_branch_product_name(self, obj):
        return f"{obj.branch_product.branch.name} - {obj.branch_product.product.name}"
    
    def get_branch_product_charge_name(self, obj):
        return f"{obj.branch_product.branch.name} - {obj.branch_product.product.name} - {obj.charge.name}"
    
    def validate(self, data):
        """
        Checking if the combination of branch_product and charge is unique.
        """
        if BranchProductCharge.objects.filter(branch_product=data['branch_product'], charge=data['charge']).exists():
            raise serializers.ValidationError("This branch product charge combination already exists.")
        return data
