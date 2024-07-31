from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) > 25:
            raise ValidationError(_("The password cannot exceed 25 characters."), code="password_too_long")
        if not any(char.isdigit() for char in password):
            raise ValidationError(_("The password must contain at least one digit."), code="password_no_digit")

    def get_help_text(self):
        return _("Your password must contain at least one digit and cannot exceed 25 characters.")