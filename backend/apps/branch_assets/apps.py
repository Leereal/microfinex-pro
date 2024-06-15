from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class BranchAssetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.branch_assets"
    verbose_name = _("Branch Assets") #Meta option to create human readable name of the object in singular

