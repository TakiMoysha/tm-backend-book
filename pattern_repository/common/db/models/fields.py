from typing import Any, TypeAlias

from django.db.models import EmailField, Field, SlugField

StrOrNone: TypeAlias = str | None


class SaveAsLowerCaseMixin(Field[StrOrNone, str]):
    def get_prep_value(self, value: Any) -> Any:
        value = super().get_prep_value(value)
        return value.lower() if value is not None else value


class LowerEmailField(EmailField[StrOrNone, str], SaveAsLowerCaseMixin):
    ...


class LowerSlugField(SlugField[StrOrNone, str], SaveAsLowerCaseMixin):
    ...
