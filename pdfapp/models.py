from django.db import models
from .validators import validate_pdf_extension


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d',
                               validators=[validate_pdf_extension])
    ready_html = False
    processing_html = False
