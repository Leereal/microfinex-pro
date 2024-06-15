from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class LoanStatusesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.loan_statuses"
    verbose_name = _("Loan Statuses") #Meta option to create human readable name of the object in singular

