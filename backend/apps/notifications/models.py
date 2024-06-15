from django.db import models
from django.contrib.auth import get_user_model
from apps.common.models import TimeStampedModel
from apps.branches.models import Branch

User = get_user_model()

class Notifications(TimeStampedModel):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sent_notifications', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    message = models.TextField()
    is_viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification {self.id} - Receiver: {self.receiver}, Sender: {self.sender}, Branch: {self.branch}"
