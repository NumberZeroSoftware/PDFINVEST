from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import os

from datetime import datetime,date

# Validates that a file given has PDF extension.
def validate_pdf_extension(value):
    extension = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not extension.lower() in valid_extensions:
        raise ValidationError(u'Tipo de archivo no soportado.')

# Validates that a given integer is positive or zero.
def validate_positive_integer(value):
    if value < 0:
        raise ValidationError(
            _('Número, %(value)s, deberia ser mayor o igual que cero'),
            params={'value': value},
        )

# Validates that a given integer is positive.
def validate_non_zero(value):
    if value < 0:
        raise ValidationError(
            _('Número, %(value)s, deberia ser mayor que cero'),
            params={'value': value},
        )


# Validates that an integer given is between 0 and 16.
def validate_credits(value):
    if value < 0 or value > 16:
        raise ValidationError(
            _('%(value)s Creditos deberian estar entre cero y dieciseis'),
            params={'value': value},
        )

# Validates that an integer given is between 1 and 31.
def validate_days_month(value):
    if value < 1 or value > 31:
        raise ValidationError(
            _('Número %(value)s debe estar entre 1 y 31'),
            params={'value': value},
        )

# Validates that an integer given is between 1969 and the actual year.
def validate_program_years(value):
    if value < 1969 or value > date.today().year + settings.FUTURE_YEARS:
        raise ValidationError(
            _('El año %(value)s debe estar entre 1969 y %(year)s'),
            params={'value': value, 'year': date.today().year + settings.FUTURE_YEARS},
        )

# Validates that an integer given is between 1900 and the actual year.
def validate_years(value):
    if value < 1900 or value > date.today().year:
        raise ValidationError(
            _('El año %(value)s debe estar entre 1900 y %(year)s'),
            params={'value': value, 'year': date.today().year},
        )
