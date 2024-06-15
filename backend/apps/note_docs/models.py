from django.db import models
from apps.common.models import TimeStampedModel

class NoteDoc(TimeStampedModel):
    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
