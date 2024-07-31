from typing import Tuple

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import (
    TimeStampedModel,
    ActivationBaseModel,
)
from .managers import UserManager

GENDER_CHOICES: Tuple[Tuple[str, ...], ...] = (
    ("empty", _("Empty")),
    ("man", _("Man")),
    ("woman", _("Woman")),
)


class User(AbstractUser, TimeStampedModel, ActivationBaseModel):
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(blank=True, null=True, max_length=150, unique=True)
    birth_date = models.DateField(_("Birth Date"), null=True, blank=True)
    gender = models.CharField(_("Gender"), choices=GENDER_CHOICES, default=GENDER_CHOICES[0][0], max_length=5)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-created_at"]

    def __str__(self):
        fields = [self.username, self.first_name, self.last_name]
        fields = list(filter(lambda x: x, fields))
        fields = list(map(lambda x: str(x), fields))
        return " | ".join(fields)

    def get_pronouns(self) -> str:
        return self.last_name + " " + self.first_name[0] + "."
