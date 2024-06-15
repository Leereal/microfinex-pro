from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedModel

class DurationUnits(models.TextChoices):
    DAYS = 'DAYS', _('Days')
    WEEKS = 'WEEKS', _('Weeks')
    MONTHS = 'MONTHS', _('Months')
    YEARS = 'YEARS', _('Years')

class Period(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name")
    )    
    duration = models.IntegerField(
        verbose_name=_("Duration"),
        help_text=_("Duration of the period in units specified by 'Duration Unit'.")
    )
    duration_unit = models.CharField(
        max_length=10,
        choices=DurationUnits.choices,
        default=DurationUnits.MONTHS,
        verbose_name=_("Duration Unit"),
        help_text=_("Unit of measurement for the period's duration.")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,  
        null=True
    )

    class Meta:
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")

    def __str__(self):
        return self.name
