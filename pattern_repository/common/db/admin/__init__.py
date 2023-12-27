from typing import TypeVar

from common.db.models import Model
from django.contrib.admin import ModelAdmin as DjModelAdmin

_ModelType = TypeVar("_ModelType", bound=Model)
# _ChildModelType = TypeVar("_ChildModelType", bound=Model)
# _ParentModelType = TypeVar("_ParentModelType", bound=Model)


class ModelAdmin(DjModelAdmin[_ModelType]):
    pass

