from django.db import models

from ..base.models import BaseRegistry

class RegistryGroup(models.Model):
    registry = models.ForeignKey(BaseRegistry, on_delete=models.CASCADE)
