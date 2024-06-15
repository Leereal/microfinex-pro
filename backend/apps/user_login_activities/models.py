from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateField(auto_now_add=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True, default=None)
    user_agent = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.user} - {self.login_date}"
