from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GlobalSettingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.global_settings"
    verbose_name = _("Global Settings") #Meta option to create human readable name of the object in singular
