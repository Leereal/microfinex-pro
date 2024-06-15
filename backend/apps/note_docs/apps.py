from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class NoteDocsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.note_docs"
    verbose_name = _("Note Docs") #Meta option to create human readable name of the object in singular
