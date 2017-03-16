from django.test import TestCase

from django.db import models
from pdfapp.models import Division
from pdfapp.models import Deanery
from pdfapp.models import Department
from pdfapp.models import Coordination
from pdfapp.models import Program
from pdfapp.models import Document
from django.core.exceptions import ValidationError

class TestProgram(TestCase):

    # Prueba de esquina: Código numérico muy largo.
    def test_number_long(self):
        with self.assertRaises(Exception):
            Program.objects.create(number="12345")

    # Prueba de borde: Tamaño máximo del código numérico.
    def test_number_max(self):
            Program.objects.create(number="1234")

    # Prueba de esquina: Código numérico muy corto.
    def test_number_short(self):
        with self.assertRaises(Exception):
            Program.objects.create(number="12")

    # Prueba de borde: Tamaño mínimo del código numérico.
    def test_number_min(self):
            Program.objects.create(number="123")

    # Prueba de esquina: Créditos negativos.
    def test_credits_neg(self):
        with self.assertRaises(Exception):
            Program.objects.create(credits=-1)

    # Prueba de borde: Créditos mínimos.
    def test_credits_min(self):
        Program.objects.create(credits=0)

    # Prueba de borde: Créditos máximo.
    def test_credits_max(self):
        Program.objects.create(credits=16)

    # Prueba de esquina: Demasiados créditos.
    def test_credits_big(self):
        with self.assertRaises(Exception):
            Program.objects.create(credits=17)

    # Prueba de esquina: Horas negativas.
    def test_theory_hours_neg(self):
        with self.assertRaises(Exception):
            Program.objects.create(theory_hours=-1)

    def test_practice_hours_neg(self):
        with self.assertRaises(Exception):
            Program.objects.create(practice_hours=-1)

    def test_laboratory_hours_neg(self):
        with self.assertRaises(Exception):
            Program.objects.create(laboratory_hours=-1)

    # Prueba de esquina: Horas totales en cero.
    def test_zero_hours(self):
        with self.assertRaises(Exception):
            Program.objects.create(theory_hours=0, 
                                    practice_hours=0, 
                                    laboratory_hours=0)

    # Prueba de borde: Alguna hora en cero.
    def test_nonzero_hours(self):
        Program.objects.create(theory_hours=1, 
                                practice_hours=0, 
                                laboratory_hours=0)

    # Prueba de esquina: Año pequeño.
    def test_small_year(self):
        with self.assertRaises(Exception):
            Program.objects.create(validity_year=1968)

    # Prueba de borde: Año mínimo.
    def test_year_min(self):
        Program.objects.create(validity_year=1969)

    # Prueba: Año actual.
    def test_year_max(self):
        Program.objects.create(validity_year=2017)

