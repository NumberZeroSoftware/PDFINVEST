from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import os

from datetime import datetime,date

def validate_pdf_extension(value):
    extension = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not extension.lower() in valid_extensions:
        raise ValidationError(u'Tipo de archivo no soportado.')

def validate_positive_integer(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s Numero deberia ser mayor o igual que cero'),
            params={'value': value},
        )

def validate_credits(value):
    if value < 0 or value > 16:
        raise ValidationError(
            _('%(value)s Credidos deberian estar entre cero y dieciseis'),
            params={'value': value},
        )

def validate_program_years(value):
    if value < 1969 or value > date.today().year + 2:
        raise ValidationError(
            _('El año %s debe estar entre 1969 y %s') % (value, date.today().year + 2)
        )
