from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserLoginActivitiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.user_login_activities"
    verbose_name = _("User Login Activities") #Meta option to create human readable name of the object in singular
