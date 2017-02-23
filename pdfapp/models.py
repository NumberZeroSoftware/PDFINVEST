from django.db import models
from .validators import validate_pdf_extension

from datetime import datetime

class Document(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', validators=[validate_pdf_extension])
    ready_html = models.BooleanField(default=False)
    processing_html = models.BooleanField(default=False)
    file_name = models.TextField(default="Error: You Need to get the Filename", blank=True)
    file_path = models.TextField(null=True, blank=True)
    

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
        ('ene-mar', 'Enero-Marzo'),
        ('abr-jul', 'Abril-Julio'),
        ('jul-ago', 'Julio-Agosto (Intensivo)'),
        ('sep-dic', 'Septiembre-Diciembre'),
    )
    document = models.OneToOneField(Document)
    code = models.CharField(max_length=10, verbose_name='Código')
    denomination = models.CharField(max_length=60, verbose_name='Denominación')
    validity_year = models.IntegerField(null=True, verbose_name='Año')
    validity_trimester = models.CharField(
        max_length=7, choices=TRIMESTER, verbose_name='Trimestre')
    theory_hours = models.IntegerField(blank=True, null=True, verbose_name='Horas de Teoría')
    practice_hours = models.IntegerField(blank=True, null=True, verbose_name='Horas de Práctica')
    laboratory_hours = models.IntegerField(blank=True, null=True, verbose_name='Horas de Laboratorio')
    credits = models.IntegerField(blank=True, null=True, verbose_name='Unidad de Créditos')
    requirements = models.TextField(blank=True, verbose_name='Requisitos')
    objectives = models.TextField(blank=True, verbose_name='Objetivos')
    synoptic_content = models.TextField(blank=True, verbose_name='Contenidos Sipnóticos')
    methodological_strategies = models.TextField(blank=True, verbose_name='Estrategias Metodológicas')
    evaluation_strategies = models.TextField(blank=True, verbose_name='Estrategias de Evaluación')
    recommended_sources = models.TextField(blank=True, verbose_name='Fuentes de Información Recomendadas')
    department = models.OneToOneField(
        Department, on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Departamento')
    coordination = models.ManyToManyField(Coordination, blank=True, verbose_name='Coordinación')
    
    def __str__(self): 
        return '%s %s' % (self.pk, self.code)
