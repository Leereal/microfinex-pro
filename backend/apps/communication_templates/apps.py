from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _



class CommunicationTemplatesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.communication_templates"
    verbose_name = _("Communication Templates") #Meta option to create human readable name of the object in singular
