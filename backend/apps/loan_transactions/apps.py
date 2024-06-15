from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class LoanTransactionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.loan_transactions"
    verbose_name = _("Loan Transactions") #Meta option to create human readable name of the object in singular
