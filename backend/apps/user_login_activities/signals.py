from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

from user_login_activities.models import UserLoginActivity

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip_address = request.META.get('REMOTE_ADDR', '')  # Get user's IP address
    user_agent = request.META.get('HTTP_USER_AGENT', '')  # Get user agent

    # Create UserLoginActivity instance
    UserLoginActivity.objects.create(
        user=user,
        ip_address=ip_address,
        user_agent=user_agent
    )
