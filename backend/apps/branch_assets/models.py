from email.policy import default
from tabnanny import verbose
from django.db import models
from apps.audits.auditing import AuditableMixin
from apps.branches.models import Branch
from apps.common.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class BranchAssets(AuditableMixin, TimeStampedModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,null=True, related_name='branch_assets')
    item = models.CharField(verbose_name=_("item"),max_length=255, validators=[MinLengthValidator(3)])
    description = models.TextField(verbose_name=_("description"),blank=True, null=True, default=None) 
    brand = models.CharField(verbose_name=_("brand"), max_length=255, default=None, blank=True, null=True)
    color = models.CharField(max_length=50, default=None, blank=True, null=True)
    quantity = models.IntegerField(verbose_name=_("quantity"),default=1)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='captured_branch_assets')
    used_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='used_assets')
    purchase_date = models.DateField(verbose_name=_("purchase date"),null=True, blank=True)
    images = models.JSONField(verbose_name=_("images"),null=True, blank=True, default=list)

    
    class Meta:
        verbose_name = _("branch")
        verbose_name_plural = _("branches")

    def __str__(self):
        return f"Branch Asset - ID: {self.id}, Item: {self.item}, Branch: {self.branch}"

    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]