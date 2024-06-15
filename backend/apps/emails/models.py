from django.db import models
from apps.common.models import TimeStampedModel

class Email(TimeStampedModel):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]

    title = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    content = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
