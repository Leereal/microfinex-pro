from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class BranchProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.branch_products"
    verbose_name = _("Branch Products") #Meta option to create human readable name of the object in singular
