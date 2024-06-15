from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class LoanApplicationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.loan_applications"
    verbose_name = _("Loan Applications") #Meta option to create human readable name of the object in singular
