from django.db import models

from ..base.models import BaseRegistry

class Company(BaseRegistry):
    name = models.CharField(max_length=32)

