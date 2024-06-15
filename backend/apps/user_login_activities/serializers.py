from rest_framework import serializers

from apps.users.serializers import UserSerializer
from .models import User, UserLoginActivity
from rest_framework.validators import UniqueForDateValidator

class UserLoginActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserLoginActivity
        fields = ['id', 'user', 'login_date', 'ip_address', 'user_agent']
        #Let's validate so that the we track the first login for the day if coming from the same ip_address
        validators = [
                UniqueForDateValidator(
                    queryset=UserLoginActivity.objects.all(),
                    field='ip_address',
                    date_field='login_date'
                )
            ]