from datetime import datetime, timezone

from common.db import models


def aware_utcnow() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


class CreatedAtMetaInfoMixin(models.Model):
    created_at = models.DateTimeField(
        null=False,
        blank=False,
        default=aware_utcnow,
        verbose_name="created at",
    )

    class Meta:
        abstract = True


class CreatedByMetaInfoMixin(models.Model):
    created_at = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="created by",
    )

    class Meta:
        abstract = True


class CreatedMetaInfoMixin(CreatedAtMetaInfoMixin, CreatedByMetaInfoMixin):
    class Meta:
        abstract = True
