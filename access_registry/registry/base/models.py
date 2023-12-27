from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models

class BaseRegistry(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    registry = GenericForeignKey('object_id')

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
