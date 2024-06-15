from django.db import models
from apps.audits.auditing import AuditableMixin
from apps.common.models import TimeStampedModel
from apps.periods.models import Period
from apps.products.models import Product
from apps.groups.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class GroupProduct(AuditableMixin, TimeStampedModel):    
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        verbose_name=_("group"),
        related_name="group_products"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        verbose_name=_("product"),
        related_name="group_products"
    )
    interest = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name=_("interest rate (%)")
    )
    max_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name=_("maximum loan amount")
    )
    min_amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        verbose_name=_("minimum loan amount")
    )
    period = models.ForeignKey(
        Period, 
        on_delete=models.CASCADE, 
        verbose_name=_("loan period")
    )
    min_period = models.IntegerField(verbose_name=_("minimum period"))
    max_period = models.IntegerField(verbose_name=_("maximum period"))
    grace_period_days = models.IntegerField(verbose_name=_("grace period in days"), default=0)
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    allow_half_period= models.BooleanField(default=False, verbose_name=_("allow half period"))
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name=_("created by")
    )


    def __str__(self):
        return f"{self.group.name} - {self.product.name}"
    
    class Meta:
        verbose_name = _("group product")
        verbose_name_plural = _("group products")
    
    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]
