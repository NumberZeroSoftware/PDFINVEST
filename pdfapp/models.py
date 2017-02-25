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
            raise ValidationError('You can\'t be ready when you\'re \
                                                     processing the html.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Document, self).save(*args, **kwargs)

class Division(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    
    def __str__(self):
        return "{}".format(self.name)


class Department(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    
    def __str__(self):
        return "{}".format(self.name)


class Deanery(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    
    def __str__(self):
        return "{}".format(self.name)


class Coordination(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    deanery = models.ManyToManyField(Deanery)
    
    def __str__(self):
        return "{}".format(self.name)


class Program(models.Model):
    TRIMESTER = (
        ('1: ene-mar', 'Enero-Marzo'),
        ('2: abr-jul', 'Abril-Julio'),
        ('3: jul-ago', 'Julio-Agosto (Intensivo)'),
        ('4: sep-dic', 'Septiembre-Diciembre'),
    )
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, verbose_name='Código')
    denomination = models.CharField(max_length=60, verbose_name='Denominación')
    validity_year = models.IntegerField(null=True, verbose_name='Año',
                                        validators=[validate_program_years])
    validity_trimester = models.CharField(max_length=10,
                                          choices=TRIMESTER,
                                          verbose_name='Trimestre')
    theory_hours = models.IntegerField(blank=True, null=True, 
                                       verbose_name='Horas de Teoría',
                                       validators=[validate_positive_integer])
    practice_hours = models.IntegerField(blank=True, null=True,
                                         verbose_name='Horas de Práctica',
                                         validators=[validate_positive_integer])
    laboratory_hours = models.IntegerField(blank=True, null=True,
                                           verbose_name='Horas de Laboratorio',
                                           validators=[validate_positive_integer])
    credits = models.IntegerField(blank=True, null=True,
                                  verbose_name='Unidad de Créditos',
                                  validators=[validate_credits])
    requirements = models.TextField(blank=True, null=True, verbose_name='Requisitos')
    objectives = models.TextField(blank=True, null=True, verbose_name='Objetivos')
    synoptic_content = models.TextField(blank=True, null=True,
                                        verbose_name='Contenidos Sipnóticos')
    methodological_strategies = models.TextField(blank=True, null=True,
                                                 verbose_name='Estrategias Metodológicas')
    evaluation_strategies = models.TextField(blank=True, null=True,
                                             verbose_name='Estrategias de Evaluación')
    recommended_sources = models.TextField(blank=True, null=True,
                                           verbose_name='Fuentes de Información Recomendadas')
    department = models.OneToOneField(Department, on_delete=models.CASCADE,
                                      blank=True, null=True, verbose_name='Departamento')
    coordination = models.ManyToManyField(Coordination, blank=True,
                                          verbose_name='Coordinación')

    def clean(self):
        hours_sum = 0
        if self.theory_hours is not None:
            hours_sum = hours_sum + self.theory_hours
        if self.practice_hours is not None:
            hours_sum = hours_sum + self.practice_hours
        if self.laboratory_hours is not None:
            hours_sum = hours_sum + self.laboratory_hours 
        if hours_sum <= 0 and not (self.theory_hours is None and self.practice_hours is None and self.laboratory_hours is None):
            raise ValidationError('The sum of the total hours must be positive.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Program, self).save(*args, **kwargs)
    
    def __str__(self): 
        return '%s %s' % (self.pk, self.code)
    
