from django.db import models

from ..base.models import Registry

class RegistryGroup(models.Model):
    registry = models.ForeignKey(Registry, on_delete=models.CASCADE)
