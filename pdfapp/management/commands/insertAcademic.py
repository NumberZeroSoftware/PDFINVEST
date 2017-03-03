"""
Command to insert the necessary academic units into the database.
Made by Carlos Infante
Last edit 02/23/2017
"""
from django.core.management.base import BaseCommand
from django.db import models
from pdfapp.models import Division
from pdfapp.models import Deanery
from pdfapp.models import Department
from pdfapp.models import Coordination

import sys

class Command(BaseCommand):
    help="Insert divisions, deaneries, departments and coordinations into the database"
    def handle(self, *args, **options):
        print("Please, ONLY run this one time. Else you will be inserting them manually")
        print("Do you want to clean the tables before insertion?")
        print("Be weary that duplicate data could be inserted otherwise")
        print("WARNING: This will wipe all data inserted into divisions, deaneries, departments and coordinations tables")
        print("Delete? (y/n): ", end="")
        ans = input()
        if (ans.lower() == "y"):
            print("DELETING")
            Division.objects.all().delete()
            Deanery.objects.all().delete()
            Department.objects.all().delete()
            Coordination.objects.all().delete()
            print("Done")

        # Create divisions
        print("Adding data into the database...")
        fis_mat = Division.objects.create(name='División de Ciencias Físicas y Matemáticas')
        soc_hum = Division.objects.create(name='División de Ciencias Sociales y Humanidades')
        bio = Division.objects.create(name='División de Ciencias Biológicas')
        tec_adm = Division.objects.create(name='División de Ciencias y Tecnologías Administrativas e Industriales')

        # Create Deaneries
        gen = Deanery.objects.create(name='Decanato de Estudios Generales')
        pro = Deanery.objects.create(name='Decanato de Estudios Profesionales')
        tec = Deanery.objects.create(name='Decanato de Estudios Tecnológicos')
        post = Deanery.objects.create(name='Decanato de Estudios de Postgrado')

        # Create Departments
        d = Department.objects.create(name='Departamento de Física', division=fis_mat)
        d = Department.objects.create(name='Departamento de Química', division=fis_mat)
        d = Department.objects.create(name='Departamento de Mecánica', division=fis_mat)
        d = Department.objects.create(name='Departamento de Matemáticas Puras y Aplicadas', division=fis_mat)
        d = Department.objects.create(name='Departamento de Computación y Tecnología de la Información', division=fis_mat)
        d = Department.objects.create(name='Departamento de Cómputo Científico y Estadística', division=fis_mat)
        d = Department.objects.create(name='Departamento de Electrónica y Circuitos', division=fis_mat)
        d = Department.objects.create(name='Departamento de Termodinámica y Fenómenos de Transferencia', division=fis_mat)
        d = Department.objects.create(name='Departamento de Conversión y Transporte de Energía', division=fis_mat)
        d = Department.objects.create(name='Departamento de Procesos y Sistemas', division=fis_mat)
        d = Department.objects.create(name='Departamento de Ciencias de los Materiales', division=fis_mat)
        d = Department.objects.create(name='Departamento de Ciencias de la Tierra', division=fis_mat)

        d = Department.objects.create(name='Departamento de Ciencia y Tecnología del Comportamiento', division=soc_hum)
        d = Department.objects.create(name='Departamento de Lengua y Literatura', division=soc_hum)
        d = Department.objects.create(name='Departamento de Ciencias Económicas y Administrativas', division=soc_hum)
        d = Department.objects.create(name='Departamento de Idiomas', division=soc_hum)
        d = Department.objects.create(name='Departamento de Filosofía', division=soc_hum)
        d = Department.objects.create(name='Departamento de Ciencias Sociales', division=soc_hum)
        d = Department.objects.create(name='Departamento de Diseño Arquitectura y Artes Plásticas', division=soc_hum)
        d = Department.objects.create(name='Departamento de Planificación Urbana', division=soc_hum)

        d = Department.objects.create(name='Departamento de Biología Celular', division=bio)
        d = Department.objects.create(name='Departamento de Estudios Ambientales', division=bio)
        d = Department.objects.create(name='Departamento de Tecnología de Procesos Biológicos y Bioquímicos', division=bio)
        d = Department.objects.create(name='Departamento de Biología de Organismos', division=bio)

        d = Department.objects.create(name='Departamento de Tecnología de Servicios', division=tec_adm)
        d = Department.objects.create(name='Departamento de Tecnología Industrial', division=tec_adm)
        d = Department.objects.create(name='Departamento de Formación General y Ciencias Básicas', division=tec_adm)

        # Create Coordinations
        d = Coordination.objects.create(name='Coordinación de Ciclo Básico')
        d.deanery.add(gen)
        d = Coordination.objects.create(name='Coordinación de Ciclo Profesional')
        d.deanery.add(gen)
        d = Coordination.objects.create(name='Coordinación de Formación General')
        d.deanery.add(gen)
        d = Coordination.objects.create(name='Coordinación de Ciclo de Iniciación Universitaria')
        d.deanery.add(gen)
        d = Coordination.objects.create(name='Coordinación de Química')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Matemática')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Biología')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Física')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Tecnología e Ingeniería Eléctrica')
        d.deanery.add(pro, tec)
        d = Coordination.objects.create(name='Coordinación de Tecnología e Ingeniería Electrónica')
        d.deanery.add(pro, tec)
        d = Coordination.objects.create(name='Coordinación de Ingeniería Mecánica')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Ingeniería Química')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Ingeniería de Computación')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Ingeniería Geofísica')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Ingeniería de Materiales')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Ingeniería de Producción y Organización Empresarial')
        d.deanery.add(pro, tec)
        d = Coordination.objects.create(name='Coordinación de Tecnología Mecánica, Mantenimiento Aeronáutico e Ingeniería de Mantenimiento')
        d.deanery.add(pro, tec)
        d = Coordination.objects.create(name='Coordinación de Ingeniería de Telecomunicaciones')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Arquitectura')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Estudios Urbanos')
        d.deanery.add(pro)
        d = Coordination.objects.create(name='Coordinación de Turismo, Hotelería y Hospitalidad')
        d.deanery.add(pro, tec)
        d = Coordination.objects.create(name='Coordinación de Comercio Exterior y Licenciatura en Comercio Internacional')
        d.deanery.add(pro, tec)
        d = Coordination.objects.create(name='Coordinación de Administración Aduanera')
        d.deanery.add(tec)
        d = Coordination.objects.create(name='Coordinación de Administración del Transporte y Organización Empresarial')
        d.deanery.add(tec)
        d = Coordination.objects.create(name='Ciencias Básicas y Aplicadas')
        d.deanery.add(post)
        d = Coordination.objects.create(name='Ciencias Sociales y Humanidades')
        d.deanery.add(post)
        d = Coordination.objects.create(name='Ingeniería y Tecnología')
        d.deanery.add(post)
        print("Done")
