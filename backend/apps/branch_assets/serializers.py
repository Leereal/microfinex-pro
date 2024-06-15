from rest_framework import serializers
from apps.branches.models import Branch
from apps.users.serializers import UserSerializer
from .models import BranchAssets, User
from apps.branches.serializers import BranchSerializer

class BranchAssetSerializer(serializers.ModelSerializer):  
    # used_by = UserSerializer()
    

    def create(self, validated_data):
        # Get the logged in users active_branch_id
        current_user = self.context['request'].user

        # Get the logged in users active_branch_id
        active_branch_id = self.context['request'].user.active_branch_id        
        
        active_branch = None
        #If there is no branch in data provided then add it as the active_branch
        if 'branch' in validated_data:
            active_branch = validated_data.pop('branch')
        else:
            # Fetch the Branch instance corresponding to active_branch_id
            active_branch = Branch.objects.get(pk=active_branch_id)
        
        validated_data['branch'] = active_branch
        validated_data['user'] = current_user
        return BranchAssets.objects.create(**validated_data)

    class Meta:
        model = BranchAssets
        fields = [
            "id",
            "branch",
            "item",
            "description",
            "brand",
            "color",
            "quantity",
            "user",
            "used_by",
            "purchase_date",
            "images",
        ]
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.used_by:    
            response['used_by'] = UserSerializer(instance.used_by).data
        return response

        
     