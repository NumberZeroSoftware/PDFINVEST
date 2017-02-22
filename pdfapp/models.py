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
        ('ene-mar', 'Enero-Marzo'),
        ('abr-jul', 'Abril-Julio'),
        ('jul-ago', 'Julio-Agosto (Intensivo)'),
        ('sep-dic', 'Septiembre-Diciembre'),
    )
    document = models.OneToOneField(Document)
    code = models.CharField(max_length=10)
    denomination = models.CharField(max_length=60)
    validity_year = models.IntegerField()
    validity_trimester = models.CharField(max_length=7, choices=TRIMESTER)
    theory_hours = models.IntegerField(blank=True, null=True)
    practice_hours = models.IntegerField(blank=True, null=True)
    laboratory_hours = models.IntegerField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    requirements = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    synoptic_content = models.TextField(blank=True)
    methodological_strategies = models.TextField(blank=True)
    evaluation_strategies = models.TextField(blank=True)
    recommended_sources = models.TextField(blank=True)
    department = models.OneToOneField(Department, on_delete=models.CASCADE, blank=True, null=True)
    coordination = models.ManyToManyField(Coordination, blank=True)