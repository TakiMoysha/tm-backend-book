from django.db import models

from ..base.models import Registry

class Company(Registry):
    name = models.CharField(max_length=32)

