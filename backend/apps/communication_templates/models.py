from django.db import models
from apps.common.models import TimeStampedModel

class CommunicationTemplates(TimeStampedModel):
    class Type(models.TextChoices):
        EMAIL = 'email', 'Email'
        SMS = 'sms', 'SMS'

    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    type = models.CharField(max_length=20, choices=Type.choices)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
