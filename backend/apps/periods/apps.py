from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class PeriodsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.periods"
    verbose_name = _("Periods") #Meta option to create human readable name of the object in singular
