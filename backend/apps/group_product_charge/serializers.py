from rest_framework import serializers
from apps.group_product_charge.models import GroupProductCharge

class GroupProductChargeSerializer(serializers.ModelSerializer):
    group_product_name = serializers.SerializerMethodField()
    group_product_charge_name = serializers.SerializerMethodField()

    class Meta:
        model = GroupProductCharge
        fields = ['id', 'group_product_name', 'group_product_charge_name', 'group_product', 'charge', 'is_active']

    def get_group_product_name(self, obj):
        return str(obj.group_product)

    def get_group_product_charge_name(self, obj):
        return f"{obj.group_product} - {obj.charge.name}"
    
    def validate(self, data):
        """
        Check if the combination of group_product and charge is unique.
        """
        if GroupProductCharge.objects.filter(group_product=data['group_product'], charge=data['charge']).exists():
            raise serializers.ValidationError("This group product charge combination already exists.")
        return data
