from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.audits.auditing import AuditableMixin
from apps.charges.models import Charge
from apps.common.models import TimeStampedModel
from apps.group_product.models import GroupProduct

class GroupProductCharge(TimeStampedModel, AuditableMixin):
    group_product = models.ForeignKey(
        GroupProduct, 
        on_delete=models.CASCADE, 
        verbose_name=_('Group Product')
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
        verbose_name = _('Group Product Charge')
        verbose_name_plural = _('Group Product Charges')

    def __str__(self):
        return f"Group Product Charge - ID: {self.id}, Group Product: {self.group_product}"

    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]