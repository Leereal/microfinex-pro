from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GroupProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.group_product"
    verbose_name = _("Group Product") #Meta option to create human readable name of the object in singular
