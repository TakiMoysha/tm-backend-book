from django.db.models.deletion import RestrictedError  # noqa
from django.db.utils import IntegrityError, ProgrammingError  # noqa

class SequenceDoesNotExist(Exception):
    ...
