from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class NotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.notes"
    verbose_name = _("Notes") #Meta option to create human readable name of the object in singular
