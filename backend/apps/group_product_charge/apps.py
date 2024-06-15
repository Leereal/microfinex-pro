from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GroupProductChargeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.group_product_charge"
    verbose_name = _("Group Product Charge") #Meta option to create human readable name of the object in singular
