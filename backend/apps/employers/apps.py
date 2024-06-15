from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class EmployersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.employers"
    verbose_name = _("Employers") #Meta option to create human readable name of the object in singular
