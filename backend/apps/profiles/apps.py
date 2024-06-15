from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.profiles"
    verbose_name = _("Profiles") #Meta option to create human readable name of the object in singular

    def ready(self):
        from apps.profiles import signals