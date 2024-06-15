from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.audits.auditing import AuditableMixin
from apps.common.models import TimeStampedModel
from apps.branches.models import Branch

User = get_user_model()

class Group(AuditableMixin,TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')

    name = models.CharField(verbose_name=_("name"), max_length=255, unique=True)
    description = models.TextField(verbose_name=_("description"), null=True, blank=True)
    leader = models.CharField(verbose_name=_("leader"), max_length=255, null=True, blank=True)
    email = models.EmailField(verbose_name=_("email"), max_length=255, null=True, blank=True)
    phone = models.CharField(verbose_name=_("phone"), max_length=255, null=True, blank=True)
    is_active = models.BooleanField(verbose_name=_("is active"), default=True)
    branch = models.ForeignKey(Branch, verbose_name=_("branch"), on_delete=models.SET_NULL, related_name="groups", null=True, blank=True)
    created_by = models.ForeignKey(User, verbose_name=_("created by"), on_delete=models.SET_NULL, related_name="created_groups", null=True, blank=True)
    status = models.CharField(
        verbose_name=_("status"),
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]
