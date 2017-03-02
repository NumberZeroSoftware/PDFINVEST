from django.db import models
from .validators import validate_pdf_extension
from .validators import validate_positive_integer
from .validators import validate_credits
from .validators import validate_program_years
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from datetime import datetime


class Document(models.Model):
    # Document in PDF format to be uploaded to the page.
    
    # The date of the upload.
    date = models.DateTimeField(
        default=datetime.now,
        blank=True,
    )

    # The uploaded document. Must be in PDF format.    
    docfile = models.FileField(
        upload_to='documents/%Y/%m/%d',
        validators=[validate_pdf_extension],
    )
 
    # HTML textring of the transcript PDF document given.
    html_text_string = models.TextField(
        null=True,
        blank=True,
    )

    # This field is False until the transcription is finished.
    ready_html = models.BooleanField(
        default=False,
    )

    # This field is True while the transcription is in process.
    processing_html = models.BooleanField(
        default=False,
    )

    # The name of the PDF document file.
    file_name = models.TextField(
        default="Error: You Need to get the Filename",
        blank=True,
    )

    # Path containing the PDF document file.
    file_path = models.TextField(
        null=True,
        blank=True,
    )
    
    # Avoids to mark the trancription as ready and processing at the same time.
    def clean(self):
        if self.ready_html and self.processing_html:
            raise ValidationError('You can\'t be ready when you\'re \
                                                     processing the html.')

    # Saves Document objects into database.
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Document, self).save(*args, **kwargs)


class Division(models.Model):
    # Divisions are the academic units in charge of the departments.

    # Name of the division.
    name = models.CharField(
        max_length=60,
        primary_key=True,
    )
    
    # Returns the name of the division.
    def __str__(self):
        return "{}".format(self.name)


class Department(models.Model):
    # Departments are academic units. They usually offer the assignatures.

    # Name of the department.
    name = models.CharField(
        max_length=60,
        primary_key=True,
    )

    # A department should be subscribed to one division.
    division = models.ForeignKey(
        Division,
        on_delete=models.CASCADE,
    )
    
    # Returns the name of the department.
    def __str__(self):
        return "{}".format(self.name)


class Deanery(models.Model):
    # Deaneries are the academic units in charge of the coordinations.

    # Name of the deanery.
    name = models.CharField(
        max_length=60,
        primary_key=True,
    )

    # Returns the name of the deanery.
    def __str__(self):
        return "{}".format(self.name)


class Coordination(models.Model):
    # Coordinations are academic units. They usually manage study programs.
    # They can offer assignatures in a few cases.

    # Name of the coordination.
    name = models.CharField(
        max_length=60,
        primary_key=True,
    )

    # A coordination can be subscribed to many deaneries.
    deanery = models.ManyToManyField(
        Deanery,
    )

    # Returns the name of the coordination.
    def __str__(self):
        return "{}".format(self.name)


class Program(models.Model):
    # The program of an assignature and all its related data.

    # All posible trimesters, including the summer intensive.
    TRIMESTER = (
        ('1: ene-mar', 'Enero-Marzo'),
        ('2: abr-jul', 'Abril-Julio'),
        ('3: jul-ago', 'Julio-Agosto (Intensivo)'),
        ('4: sep-dic', 'Septiembre-Diciembre'),
    )

    # PDF document associated to the program.
    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    # The code of the assignature.
    code = models.CharField(
        blank=True, 
        max_length=10,
        verbose_name='Código',
    )

    # The name of the assignature.
    denomination = models.CharField(
        blank=True, 
        max_length=60,
        verbose_name='Denominación',
    )

    # Year of validity of the program.
    validity_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Año',
        validators=[validate_program_years],
    )

    # Trimester of validity of the program.
    validity_trimester = models.CharField(
        max_length=10,
        choices=TRIMESTER,
        blank=True, 
        null=True,
        verbose_name='Trimestre',
    )

    # Number of hours of theory in the assignature.
    theory_hours = models.PositiveIntegerField(
        blank=True,
        null=True, 
        verbose_name='Horas de Teoría',
        validators=[validate_positive_integer],
    )

    # Number of hours of practice in the assignature.
    practice_hours = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Horas de Práctica',
        validators=[validate_positive_integer],
    )

    # Number of hours of laboratory in the assignature.
    laboratory_hours = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Horas de Laboratorio',
        validators=[validate_positive_integer],
    )

    # Number of crédits in the assignature. Must be a number between 0 and 16.
    credits = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Unidad de Créditos',
        validators=[validate_credits],
    )

    # Requirements to take the course.
    requirements = models.TextField(
        blank=True,
        null=True,
        verbose_name='Requisitos',
    )

    # Objectives of the assignature.
    objectives = models.TextField(
        blank=True,
        null=True,
        verbose_name='Objetivos',
    )

    # Synoptic content of the program.
    synoptic_content = models.TextField(
        blank=True,
        null=True,
        verbose_name='Contenidos Sipnóticos',
    )

    # Methodological strategies suggested by the program.
    methodological_strategies = models.TextField(
        blank=True,
        null=True,
       verbose_name='Estrategias Metodológicas',
    )

    # Evaluation strategies suggested by the program.
    evaluation_strategies = models.TextField(
        blank=True,
        null=True,
        verbose_name='Estrategias de Evaluación',
    )

    # Recommended sources of information.
    recommended_sources = models.TextField(
        blank=True,
        null=True,
        verbose_name='Fuentes de Información Recomendadas',
    )

    # Departament in charge of the assignature.
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Departamento',
    )

    # Coordinations in chharge of the program.
    coordination = models.ManyToManyField(
        Coordination,
        blank=True,
        verbose_name='Coordinación',
    )

    # Checks the that the sum of the hours is positive.
    def clean(self):
        hours_sum = 0
        if self.theory_hours is not None:
            hours_sum = hours_sum + self.theory_hours
        if self.practice_hours is not None:
            hours_sum = hours_sum + self.practice_hours
        if self.laboratory_hours is not None:
            hours_sum = hours_sum + self.laboratory_hours 
        if (hours_sum < 0 or hours_sum > 40) and \
            not (self.theory_hours is None and self.practice_hours is None and self.laboratory_hours is None):
            raise ValidationError('The sum of the total hours must be less or equal to fourty and positive or equal to zero. \
                Or the three of them must not be set.')

    # Saves Program objects into the database.
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Program, self).save(*args, **kwargs)

    # Returns the primary key for the program and the code.
    def __str__(self): 
        return '%s %s' % (self.pk, self.code)
    
