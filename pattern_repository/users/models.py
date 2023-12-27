from typing import Any
from django.contrib.auth.models import AbstractBaseUser, UserManager

from common.db import models

class User(AbstractBaseUser):
    email = models.LowerEmailField(max_length=255, null=False, blank=False, unique=True, verbose_name="email address")

    is_active = models.BooleanField(null=False, default=True, blank=True, verbose_name="active")
    is_superuser = models.BooleanField(null=False, default=False, blank=True, verbose_name="superuser")

    created_at = models.DateTimeField(null=False, auto_now_add=True, verbose_name="created at")
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name="verified at")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["email"]

    def __str__(self) -> str:
        return self.email

    def __repr__(self) -> str:
        return f"<User(email={self.email})>"

    @property
    def is_staff(self) -> bool:
        return self.is_superuser


