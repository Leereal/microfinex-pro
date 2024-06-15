from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ChargesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.charges"
    verbose_name = _("Charges") #Meta option to create human readable name of the object in singular
