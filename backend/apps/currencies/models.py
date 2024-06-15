from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.audits.auditing import AuditableMixin
from apps.common.models import TimeStampedModel

class Currency(AuditableMixin,TimeStampedModel):
    class Type(models.TextChoices):
        BEFORE = 'before', _('Before')
        AFTER = 'after', _('After')
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, unique=True)
    symbol = models.CharField(max_length=10, unique=True)
    position = models.CharField(max_length=10, default="before")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("currency")
        verbose_name_plural = _("currencies") 

    def __str__(self):
        return self.name
    
    def get_audit_fields(self):
        # Dynamically retrieve all field names from the model
        return [field.name for field in self._meta.fields]
