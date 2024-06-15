from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DocumentTypesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.document_types"
    verbose_name = _("Document Types") #Meta option to create human readable name of the object in singular
