from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedMeta:
    abstract = True
    ordering = ["-created_at", "-modified_at"]


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("Created"), auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(_("Modified"), auto_now=True)

    @property
    def ago(self):
        return (timezone.now() - self.created_at).total_seconds()

    Meta = TimeStampedMeta

    def __str__(self):
        return f"{self.created_at}, {self.modified_at}"


class ActivationBaseModel(models.Model):
    is_active = models.BooleanField(_("Is Active?"), default=True)

    class Meta:
        abstract = True

    def activate(self):
        self.is_active = True
        self.save(update_fields=("is_active",))

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=("is_active",))


class PhoneNumberBaseModel(models.Model):
    ACCOUNT_PHONE_REGEX = r"\+77\d{9}$"
    ACCOUNT_PHONE_REGEX_MESSAGE = _(
        "Phone number must be entered in the format: '+77777777777'. Up to 11 digits allowed."
    )

    phone_regex = RegexValidator(regex=ACCOUNT_PHONE_REGEX, message=ACCOUNT_PHONE_REGEX_MESSAGE)
    phone_number = models.CharField(_("Phone number"), max_length=12, validators=(phone_regex,))

    class Meta:
        abstract = True
