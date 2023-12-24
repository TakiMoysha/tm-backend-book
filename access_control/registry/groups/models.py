from django.contrib.contenttypes.fields import GenericForeignKey

from common.db import models
from common.db.mixins import CreatedAtMetaInfoMixin

class RegistryGroupMember(models.BaseModel, CreatedAtMetaInfoMixin):
    registry = models.ForeignKey("registry.Registry", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "registry group member"
        verbose_name_plural = "registry group members"
        constraints = [
            models.UniqueConstraint(fields=["registry", "user"], name="%(app_label)s_%(class)s_unique_registry_group_member")
        ]
        indexes = [
            models.Index(fields=["registry", "user"]),
        ]
        ordering = ["registry", "user"]

