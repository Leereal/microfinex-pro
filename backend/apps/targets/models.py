from django.db import models
from apps.common.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Targets(TimeStampedModel):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    month_year = models.DateField()
    is_reached = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Target - ID: {self.id}, Branch: {self.branch}, Month/Year: {self.month_year}"
