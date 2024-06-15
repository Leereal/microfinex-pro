from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class TargetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.targets"
    verbose_name = _("Targets") #Meta option to create human readable name of the object in singular
