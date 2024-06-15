from django.contrib import admin
from .models import UserLoginActivity

@admin.register(UserLoginActivity)
class UserLoginActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_date', 'ip_address', 'user_agent')
    list_filter = ('login_date','user')
    search_fields = ('user__email', 'ip_address', 'user_agent')
