from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from common.db import models


class Registry(models.Model):
    # GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    registry = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
