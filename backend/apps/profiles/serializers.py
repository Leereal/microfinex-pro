from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    profile_photo = serializers.SerializerMethodField()
    branches = serializers.SerializerMethodField() 

    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "profile_photo",
            "phone",
            "gender",
            "branches",    
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_profile_photo(self, obj):
        return obj.profile_photo.url if obj.profile_photo else None
    
    def get_branches(self, obj):
        user = getattr(obj, 'user', None)  # Retrieve the user object from the profile
        if user:
            branches = user.branches.all()  # Retrieve the related branches
            return [branch.name for branch in branches]  # Assuming branch model has a name attribute
        else:
            return []  # Return an empty list if no user or no branches are found


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        #Fields that will be allowed update
        fields = [
            "phone",
            "profile_photo",    
            "gender"
        ]