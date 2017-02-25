from django.db import models
from .validators import validate_pdf_extension
from .validators import validate_positive_integer
from .validators import validate_credits
from .validators import validate_program_years
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from datetime import datetime


class Document(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', validators=[validate_pdf_extension])
    html_text_string = models.TextField(null=True, blank=True)
    ready_html = models.BooleanField(default=False)
    processing_html = models.BooleanField(default=False)
    file_name = models.TextField(default="Error: You Need to get the Filename", blank=True)
    file_path = models.TextField(null=True, blank=True)

    def clean(self):
        if self.ready_html and self.processing_html:
            raise django_excetions.ValidationError('You can\'t be ready when you\'re \
                                                     processing the html.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Document, self).save(*args, **kwargs)

class Division(models.Model):
    name = models.CharField(max_length=60, primary_key=True)

class Department(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

class Deanery(models.Model):
    name = models.CharField(max_length=60, primary_key=True)

class Coordination(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    deanery = models.ManyToManyField(Deanery)

class Program(models.Model):
    TRIMESTER = (
        ('1: ene-mar', 'Enero-Marzo'),
        ('2: abr-jul', 'Abril-Julio'),
        ('3: jul-ago', 'Julio-Agosto (Intensivo)'),
        ('4: sep-dic', 'Septiembre-Diciembre'),
    )
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    denomination = models.CharField(max_length=60)
    validity_year = models.IntegerField(validators=[validate_program_years])
    validity_trimester = models.CharField(max_length=7, choices=TRIMESTER)
    theory_hours = models.IntegerField(blank=True, null=True, validators=[validate_positive_integer])
    practice_hours = models.IntegerField(blank=True, null=True, validators=[validate_positive_integer])
    laboratory_hours = models.IntegerField(blank=True, null=True, validators=[validate_positive_integer])
    credits = models.IntegerField(blank=True, null=True, validators=[validate_credits])
    requirements = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    synoptic_content = models.TextField(blank=True, null=True)
    methodological_strategies = models.TextField(blank=True, null=True)
    evaluation_strategies = models.TextField(blank=True, null=True)
    recommended_sources = models.TextField(blank=True, null=True)
    department = models.OneToOneField(Department, on_delete=models.CASCADE, blank=True, null=True)
    coordination = models.ManyToManyField(Coordination, blank=True)

    def clean(self):
        if self.theory_hours + self.practice_hours + self.practice_hours <= 0:
            raise django_excetions.ValidationError('The sum of the total hours must be positive.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Program, self).save(*args, **kwargs)
