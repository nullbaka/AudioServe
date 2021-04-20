from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import json


def validate_participants(value):
    value = json.loads(value)
    if len(value) > 10:
        raise ValidationError(
            _('%(value)s can contain maximum 10 items'),
            params={'value': value},
        )
    for val in value:
        if len(val) > 100:
            raise ValidationError(
            _('maximum length of item can only be 100: %(val)s '),
            params={'val': val},
        )
