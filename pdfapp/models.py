from django.db import models
from .validators import validate_pdf_extension
from .validators import validate_positive_integer
from .validators import validate_credits
from .validators import validate_program_years
from .validators import validate_non_zero
from .validators import validate_days_month
from .validators import validate_years
from .validators import validate_max_hours
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from datetime import datetime, date
import re



class Document(models.Model):
    # Document in PDF format to be uploaded to the page.
    
    RE_COURSE_CODE_A = '[A-Z]{2}[ \-]?[0-9]{4}'
    RE_COURSE_CODE_B = '[A-Z]{3}[ \-]?[0-9]{3}'
    
    # The date of the upload.
    date = models.DateTimeField(
        default=datetime.now,
        blank=True,
    )

    # Chosen name of the document.
    name = models.CharField(
        max_length=60,
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
    
    # Returns a set of courses codes from an html file
    @staticmethod
    def course_codes(filename):
        html_file = open(filename, 'r')
        file_contents = html_file.read()
        possible_codes_a = re.findall(Document.RE_COURSE_CODE_A ,file_contents)
        possible_codes_b = re.findall(Document.RE_COURSE_CODE_B ,file_contents)
        possible_codes = set(possible_codes_a + possible_codes_b)
        return possible_codes
    
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

class AdditionalName(models.Model):
    # Additional fields names to be added into programs.

    # Name of the field
    name = models.CharField(
        max_length=30,
        unique=True,
    )

    def __str__(self):
        return "{}".format(self.name)

class AdditionalField(models.Model):
    # Additional field text.

    # Description of the field.
    description = models.TextField(
        null=True,
        blank=True,
    )

    # Name of the field.
    name = models.ForeignKey(
        AdditionalName,
        on_delete=models.CASCADE,
    )

class Code(models.Model):
    # Code.
    code = models.CharField(
        max_length=3,
        primary_key=True,
        verbose_name='Código',
    )
    # A department is responsible for many codes.
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "{}".format(self.code)

# Autors of recommended sources.
class Author(models.Model):
    first_name = models.CharField(
        max_length=20,
        verbose_name='Primer nombre',
    )

    second_name = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Segundo nombre',
    )

    first_surname = models.CharField(
        max_length=20,
        verbose_name='Primer apellido',
    )

    second_surname = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Segundo apelido',
    )
    def __str__(self): 
        return self.first_surname
    class Meta:
        ordering = ['first_surname','first_name']

# Recommended sources.
class Reference(models.Model):
    # Author of the author's book.
    author = models.ManyToManyField(
        Author,
        blank=True,
        verbose_name='Autor',
    )

    # Book's title.
    title = models.TextField(
        verbose_name='Título',
    )

    # Publishing house of the book.
    editorial = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Editorial',
    )

    # Recommended edition.
    edition_number = models.IntegerField(
        validators=[validate_non_zero],
        blank=True,
        null=True,
        verbose_name='No. Edición',
    )


    # Recommended year.
    year = models.IntegerField(
        validators=[validate_years],
        blank=True,
        null=True,
        verbose_name='Año',
    )

class Program(models.Model):
    # The program of an assignature and all its related data.

    # All posible trimesters, including the summer intensive.
    TRIMESTER = (
        ('0Ene-Mar', 'Enero-Marzo'),
        ('1Abr-Jul', 'Abril-Julio'),
        ('2Jul-Ago', 'Julio-Agosto (Intensivo)'),
        ('3Sep-Dic', 'Septiembre-Diciembre'),
    )
    MONTH = (
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre'),
    )

    # PDF document associated to the program.
    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    # The code of the assignature, divided in its department code and a number.
    code = models.ForeignKey(
        Code,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Código Departamento',
    )
    number = models.CharField(
        max_length=4,
        blank=True,
        validators=[RegexValidator(regex='^\d{3,4}$',
                    message='Debe estar formado por 3 o 4 dígitos.')],
        verbose_name='Código Número',
    )

    # The suggested code is approved.
    approved_code = models.BooleanField(
        default=False,
    )

    # The name of the assignature.
    denomination = models.CharField(
        blank=True, 
        max_length=60,
        verbose_name='Denominación',
    )

    # Date of validity.
    validity_date_y = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Año',
        validators=[validate_program_years]
    )
    validity_date_m = models.PositiveIntegerField(
        choices=MONTH,
        blank=True,
        null=True,
        verbose_name='Mes',
    )

    validity_date_d = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Día',
        validators=[validate_days_month],
    )

    # Proposed year of validity of the program.
    validity_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Año propuesto',
        validators=[validate_program_years],
    )

    # Proposed trimester of validity of the program.
    validity_trimester = models.CharField(
        max_length=10,
        choices=TRIMESTER,
        blank=True, 
        null=True,
        verbose_name='Trimestre propuesto',
    )

    # Number of hours of theory in the assignature.
    theory_hours = models.PositiveIntegerField(
        blank=True,
        null=True, 
        verbose_name='Horas de Teoría',
        validators=[validate_positive_integer, validate_max_hours],
    )

    # Number of hours of practice in the assignature.
    practice_hours = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Horas de Práctica',
        validators=[validate_positive_integer, validate_max_hours],
    )

    # Number of hours of laboratory in the assignature.
    laboratory_hours = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Horas de Laboratorio',
        validators=[validate_positive_integer, validate_max_hours],
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

    # General objectives of the assignature.
    objectives = models.TextField(
        blank=True,
        null=True,
        verbose_name='Objetivos Generales',
    )

    # Specific objectives of the assignature.
    specific_objectives = models.TextField(
        blank=True,
        null=True,
        verbose_name='Objetivos Específicos',
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
    recommended_sources = models.ManyToManyField(
        Reference,
        blank=True,
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

    # True if the document is ready.
    passes = models.BooleanField(
        default=False,
        verbose_name='Enviar para aprobar',
    )

    # Additional fields.
    additional_fields = models.ManyToManyField(
        AdditionalField,
        blank=True,
    )

    #Checks day, month, year to see if they form a valid date.
    def valid_date(self, d, m, y):
        if (m == None or y == None):
            return True
        try:
            d = date(y, m, d)
            return True
        except ValueError:
            return False

    #Checks if complete.
    def completed(self):
        return (self.code and self.number and self.denomination and \
                self.validity_year and self.validity_trimester and \
                (self.theory_hours or self.practice_hours or \
                self.laboratory_hours) and self.credits and \
                self.requirements and self.objectives and \
                self.synoptic_content and  self.methodological_strategies and \
                self.evaluation_strategies and self.recommended_sources and \
                self.department)

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
            raise ValidationError('La suma de las horas debe ser no negativa y menor que cuarenta.')
        if not self.valid_date(self.validity_date_d, self.validity_date_m, self.validity_date_y):
            raise ValidationError('La fecha de validación del programa no es una fecha válida.')
        if self.passes and not self.completed():
            raise ValidationError('Faltan campos por ser llenados para pasar el programa.')

    # Saves Program objects into the database.
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Program, self).save(*args, **kwargs)

    # Returns the primary key for the program and the code.
    def __str__(self): 
        return '%s %s' % (self.pk, self.code)

################################################################################
################################################################################
################################################################################
################################################################################



# Base de datos del repositorio SIGPAE.



################################################################################
################################################################################
################################################################################
################################################################################

class Programa(models.Model):
    # Crea una tabla con el programa completo asociado.
    
    TRIMESTRE = (
        ('0Ene-Mar', 'Enero-Marzo'),
        ('1Abr-Jul', 'Abril-Julio'),
        ('2Jul-Ago', 'Julio-Agosto (Intensivo)'),
        ('3Sep-Dic', 'Septiembre-Diciembre'),
    )

    codigo = models.CharField(
        max_length=6,
        verbose_name='Código',
    )


    #Nombre de la asignatura
    denominacion = models.TextField(
        blank=True,
        verbose_name='Denominación',
    )
    

    # Cantidad de créditos de la asignatura.
    creditos = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Créditos'
    )

    # Numero de horas de teoria de una asignatura.
    
    h_teoria = models.PositiveIntegerField(
        blank=True,
        null=True, 
        verbose_name='Horas de Teoría',
    )

    # Numero de horas de practica de una asignatura.

    h_prac = models.PositiveIntegerField(
        blank=True,
        null=True, 
        verbose_name='Horas de Práctica',
    )

    # Numero de horas de laboratorio de una asignatura. 

    h_lab = models.PositiveIntegerField(
        blank=True,
        null=True, 
        verbose_name='Horas de Laboratorio',
    )

    # Year of validity of the program.

    fecha_vigAno = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Año',
    )


    # Fecha de vigencia de un trimestre

    fecha_vigTrim = models.CharField(
        blank=True,
        null=True,
        choices=TRIMESTRE,
        max_length=8,
        verbose_name='Fecha Vigencia Trimestre',
    )

    # Objetivo general de la asignatura.
    obj_g = models.TextField(
        blank=True,
        null=True,
        verbose_name='Objetivo general',
    )

    # Objetivos especificos de la asignatura.
    obj_e = models.TextField(
        blank=True,
        null=True,
        verbose_name='Objetivo específico',
    )

    # Contenidos de la asignatura.
    contenidos = models.TextField(
        blank=True,
        null=True,
        verbose_name='Contenidos',
    )

    # Estrategias de la asignatura.
    estrategias = models.TextField(
        blank=True,
        null=True,
        verbose_name='Estrategias',
    )

    # Estrategias evaluativas de la asignatura.
    estrat_eval = models.TextField(
        blank=True,
        null=True,
        verbose_name='Estrategias evaluativas',
    )


    # Fuentes de la asignatura. 
    fuentes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Fuentes',
    )

    # Cronograma de la asignatura. 
    cronograma = models.TextField(
        blank=True,
        null=True,
        verbose_name='Cronograma',
    )

    # Contenido Sinoptico de la asignatura. 
    sinoptico = models.TextField(
        blank=True,
        null=True,
        verbose_name='Contenidos Sipnóticos',
    )

    # Returns the primary key for the program and the code.
    def __str__(self): 
        return '%s %s %s %s' % (self.pk, self.codigo,self.fecha_vigAno,self.fecha_vigTrim)

    # Get Every field name and value
    def __iter__(self):
        for field in self._meta.fields:
            if field.verbose_name == "ID":
                continue
            elif field.verbose_name == "Fecha Vigencia Trimestre":
                out = False
                for choice in Programa.TRIMESTRE:
                    if field.value_to_string(self) == choice[0]:
                        yield (field.verbose_name, choice[1])
                        out = True
                if not out:
                    yield (field.verbose_name, field.value_to_string(self))
            else:
                yield (field.verbose_name, field.value_to_string(self))

class Solicitud(models.Model):

    # Crea una solicitud de un programa (entidad debil).

    # Nombre de la coordinacion asociada.
    nomcoord = models.CharField(
        max_length=50,
        verbose_name='Nombre Coordinacion',
    )

    # Programa por Asignar un profesor.
    porasignar = models.BooleanField(
        default=True,
    )

    # Programa por validar departamento.
    porvalidarD = models.BooleanField(
        default=True,
    )

    # Programa rechazado por coordinacion.
    rechazadoC = models.BooleanField(
        default=False,
    )

    # Programa validado por Coordinacion.
    validadoC = models.BooleanField(
        default=False,
    )

    # Programa enviado a Dace.

    enviadoD = models.BooleanField(
        default=False,
    )

    # Programa devuelto a Dace.
    devueltoDace = models.BooleanField(
        default=False,
    )

    # Fecha de elaboracion de la solicitud
    fechaelab = models.DateTimeField(
        default=datetime.now,
    )

    # Creditos del programa
    credits = models.BooleanField(
        verbose_name='Unidad de Créditos',
    )

    # Horas de teoria de una asignatura.
    
    h_teoria = models.BooleanField(
        default=False,
        verbose_name='Horas de Teoría',
    )

    # Hras de practica de una asignatura.

    h_prac = models.BooleanField(
        default=False,
        verbose_name='Horas de Práctica',
    )

    #Horas de laboratorio de una asignatura. 

    h_lab = models.BooleanField(
        default=False,
        verbose_name='Horas de Teoría',
    )

    # Trimestre del programa.
    trime = models.CharField(
        max_length=8,
        verbose_name='Trimestre',
    )

    # Ano del programa.
    ano = models.CharField(
        max_length=8,
        verbose_name='Año',
    )

    # Creditos de requisito del programa.
    requisito_cre = models.BooleanField(
        default=False,
        verbose_name='Requisitos',
    )

    # Permisos de la coordinacion del programa.
    permiso_coord = models.BooleanField(
        default=False,
        verbose_name='Permisos',
    )

    # Tipo de las materias del programa.
    tipo_materia = models.CharField(
        max_length=20,
        verbose_name='Tipo',
    )

    # Toda solicitud se relaciona con un programa.
    programa = models.ForeignKey(
        Programa,
        on_delete=models.CASCADE,
    )

    
