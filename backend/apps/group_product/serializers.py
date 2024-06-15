from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.group_product.models import GroupProduct

User = get_user_model()

class GroupProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupProduct
        fields = [
            'id',
            'group',
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
        representation['group'] = {
            'id': instance.group.id,
            'name': instance.group.name
        }
        representation['product'] = {
            'id': instance.product.id,
            'name': instance.product.name
        }
        representation['period'] = {
            'id': instance.period.id,
            'name': instance.period.name,
            'duration': instance.period.duration,
            'duration_unit': instance.period.duration_unit
        }
        representation['created_by'] = {
            'id': instance.created_by.id,
            'full_name': instance.created_by.get_full_name
        } if instance.created_by else None
        return representation
