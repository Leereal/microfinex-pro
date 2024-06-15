from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.audits.auditing import AuditableMixin
from apps.common.models import TimeStampedModel
from apps.branch_products.models import BranchProduct
from apps.charges.models import Charge

class BranchProductCharge(TimeStampedModel, AuditableMixin):
    branch_product = models.ForeignKey(
        BranchProduct, 
        on_delete=models.CASCADE, 
        verbose_name=_('Branch Product')
    )
    charge = models.ForeignKey(
        Charge, 
        on_delete=models.CASCADE, 
        verbose_name=_('Charge')
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name=_('Is Active')
    )

    class Meta:
        verbose_name = _('Branch Product Charge')
        verbose_name_plural = _('Branch Product Charges')

    def get_branch_product_name(self):
        return f"{self.branch_product.branch.name} - {self.branch_product.product.name}"

    def __str__(self):
        return f"{self.charge.name} on {self.branch_product}"

    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]
