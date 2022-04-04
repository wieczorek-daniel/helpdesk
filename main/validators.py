from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class DigitPasswordValidator():
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not any(character.isdigit() for character in password):
            raise ValidationError(_('Password must contain at least %(min_length)d digit.') % {'min_length': self.min_length})

    def get_help_text(self):
        return _('Your password must contain at least %(min_length)d digit.') % {'min_length': self.min_length}


class UppercasePasswordValidator():
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not any(character.isupper() for character in password):
            raise ValidationError(_('Password must contain at least %(min_length)d uppercase letter.') % {'min_length': self.min_length})

    def get_help_text(self):
        return _('Your password must contain at least %(min_length)d uppercase letter.') % {'min_length': self.min_length}


class SpecialCharacterPasswordValidator():
    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        special_characters = "[.~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if not any(character in special_characters for character in password):
            raise ValidationError(_('Password must contain at least %(min_length)d special character.') % {'min_length': self.min_length})

    def get_help_text(self):
        return _('Your password must contain at least %(min_length)d special character.') % {'min_length': self.min_length}
