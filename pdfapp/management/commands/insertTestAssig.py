from django.core.management.base import BaseCommand
from django.db import models
from pdfapp.models import Programa

class Command(BaseCommand):
    help="Insert test assignatures"
    def handle(self, *args, **options):
        print("Please, ONLY run this one time. Else you will be inserting them manually")
        print("Do you want to clean the tables before insertion?")
        print("Be weary that duplicate data could be inserted otherwise")
        print("WARNING: This will wipe all data inserted into SIGPAE repository")
        print("Delete? (y/n): ", end="")
        ans = input()
        if (ans.lower() == "y"):
            print("DELETING")
            Programa.objects.all().delete()
            print("Done")

        print("Adding data into the database...")
                
        Programa.objects.create(
            codigo='MA1111',
            denominacion='Matemáticas I',
            creditos=5,
            h_teoria=30,
            h_prac=10,
            fecha_vigAno=2002,
            fecha_vigTrim='0Ene-Mar',
            obj_g='Enseñar matemáticas.',
            contenidos='Funciones, límites, derivadas.',
            estrategias='Clases presenciales y prácticas semanales.',
            estrat_eval='Tres parciales.',
            fuentes='Cálculo, Purcell, 9na edición.',
        )

        Programa.objects.create(
            codigo='CI3725',
            denominacion='Traductores e Interpretadores',
            creditos='5',
            h_teoria=30,
            h_lab=10,
            fecha_vigAno=2006,
            fecha_vigTrim='1Abr-Jul',
            obj_g='Curso de traductores.',
            contenidos='Regex, autómatas, gramáticas.',
            estrategias='Clases presenciales y proyectos de laboratorio.',
            estrat_eval='Tres parciales y un proyecto.',
            fuentes='Languages and Machines, Sudkamp, 3era edición.',
        )

        Programa.objects.create(
            codigo='LA1111',
            denominacion='Lenguajes I',
            creditos='4',
            h_teoria=30,
            fecha_vigAno=1999,
            fecha_vigTrim='0Ene-Mar',
            obj_g='Enseñar redacción a ingenieros.',
            contenidos='Estudio de distintos textos.',
            estrategias='Clases presenciales.',
            estrat_eval='Tres parciales y dos ensayos.',
            fuentes='Textos entregados por el profesor.',
        )

        Programa.objects.create(
            codigo='FS1111',
            denominacion='Física I',
            creditos='4',
            h_teoria=30,
            h_lab=10,
            fecha_vigAno=1998,
            fecha_vigTrim='3Sep-Dic',
            obj_g='Física básica.',
            contenidos='Principios de dinámia y mecánica.',
            estrategias='Clases presenciales y prácticas, demostraciones.',
            estrat_eval='Tres parciales.',
            fuentes='Física I, 10ma edición.',
        )        
        
        print("Done")
