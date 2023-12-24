from common.db import models
from registry.base.models import TreeRegistryModel


class CompanyModel(TreeRegistryModel):
    name = models.CharField(max_length=32)


class ProjectModel(TreeRegistryModel):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey(CompanyModel, null=False, on_delete=models.CASCADE)
