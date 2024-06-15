from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class PaymentGatewaysConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.payment_gateways"
    verbose_name = _("Payment Gateways") #Meta option to create human readable name of the object in singular
