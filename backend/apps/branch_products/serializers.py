from rest_framework import serializers
from .models import BranchProduct

class BranchProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchProduct
        fields = [
            'id',
            'branch',
            'product',
            'interest',
            'max_amount',
            'min_amount',
            'period',
            'min_period',
            'max_period',
            'is_active',
            'created_by',
            'created_at',
            'last_modified'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['branch'] = {
            'id': instance.branch.id,
            'name': instance.branch.name
        }
        representation['product'] = {
            'id': instance.product.id,
            'name': instance.product.name
        }
        representation['created_by'] = {
            'id': instance.created_by.id,
            'full_name': instance.created_by.get_full_name
        }
        representation['period'] = {
            'id': instance.period.id,
            'name': instance.period.name,
            'duration': instance.period.duration,
            'duration_unit': instance.period.duration_unit
        }
        return representation
