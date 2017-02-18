from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import os

def validate_pdf_extension(value):
    extension = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not extension.lower() in valid_extensions:
        raise ValidationError(u'Tipo de archivo no soportado.')