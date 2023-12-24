from django.db import models

from ..base.models import Registry

class Project(Registry):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey('registry_companies.Company', on_delete=models.CASCADE, null=True, blank=True)

