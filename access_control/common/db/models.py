import functools
import uuid

from django.db import models
from utils.uuid import encode_uuid_to_b64str


def uuid_generator() -> uuid.UUID:
    return uuid.uuid1()


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True, null=False, blank=True, default=uuid_generator, editable=False
    )

    class Meta:
        abstract = True

    @functools.cached_property
    def b64id(self) -> str:
        return encode_uuid_to_b64str(self.id)
