from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from apps.branches.models import Branch
from .models import UserBranch
from apps.branches.serializers import BranchSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()

class ListUserBranchSerializer(ListSerializer):
    def update(self, instance, validated_data):
        # Iterate over each validated data and update the corresponding instance
        for data in validated_data:
            branch_id = data.get('branch_id')
            instance_obj = self.child.Meta.model.objects.filter(user=instance.user, branch_id=branch_id).first()
            if instance_obj:
                # Update the instance with the validated data
                self.child.update(instance_obj, data)
            else:
                # Handle case when the instance doesn't exist
                self.child.create(data)
        return instance

class UserBranchSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = UserBranch
        fields = ['id','user_name','branch_name','is_active']
        list_serializer_class = ListUserBranchSerializer

        validators = [
            UniqueTogetherValidator(
                queryset=UserBranch.objects.all(),
                fields=['user', 'branch']
            )
        ]
    
    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user:
            raise ValidationError("Request or user not found in context.")
        
        validated_data['created_by'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if not request or not request.user:
            raise ValidationError("Request or user not found in context.")
        
        validated_data['created_by'] = request.user
        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="profile.gender")
    phone = PhoneNumberField(source="profile.phone")
    profile_photo = serializers.ReadOnlyField(source="profile.profile_photo.url", required=False)
    branches = BranchSerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    short_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password',)
        depth = 5      
    
    def update(self, instance, validated_data):
        branches_data = validated_data.pop('branches', None)
        user = super().update(instance, validated_data)

        if branches_data is not None:
            # Clear existing user branches
            user.user_branches.all().delete()

            # Create new user branches
            for branch_data in branches_data:
                branch_id = branch_data['branch'].id
                is_active = branch_data.get('is_active', True)
                UserBranch.objects.create(user=user, branch_id=branch_id, is_active=is_active)

        return user

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
            # Add active_branch and branches data
            representation["active_branch"] = instance.active_branch.id if instance.active_branch else None
            branches_representation = [
                {'id': branch.id, 'name': branch.name} 
                for branch in instance.branches.all()
            ]
            representation["branches"] = branches_representation
        return representation

    def get_full_name(self, obj):
        return obj.get_full_name

    def get_short_name(self, obj):
        return obj.get_short_name


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    active_branch = serializers.PrimaryKeyRelatedField(read_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    branches = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "password1": self.validated_data.get("password1", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self)
        user.save()

        setup_user_email(request, user, [])
        user.email = self.cleaned_data.get("email")
        user.password = self.cleaned_data.get("password1")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")

        return user

