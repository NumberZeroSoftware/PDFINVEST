# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 01:41
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import pdfapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pdfapp', '0021_auto_20170301_2204'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='Primer nombre')),
                ('second_name', models.CharField(blank=True, max_length=20, verbose_name='Segundo nombre')),
                ('first_surname', models.CharField(max_length=20, verbose_name='Primer apellido')),
                ('second_surname', models.CharField(blank=True, max_length=20, verbose_name='Segundo apelido')),
            ],
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pdfapp.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='Título')),
                ('editorial', models.CharField(blank=True, max_length=30, verbose_name='Editorial')),
                ('edition_number', models.IntegerField(blank=True, null=True, validators=[pdfapp.validators.validate_non_zero], verbose_name='No. Edición')),
                ('year', models.IntegerField(blank=True, null=True, validators=[pdfapp.validators.validate_years], verbose_name='Año')),
                ('author', models.ManyToManyField(to='pdfapp.Author', verbose_name='Autor')),
            ],
        ),
        migrations.AddField(
            model_name='program',
            name='approved_code',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='program',
            name='number',
            field=models.CharField(blank=True, max_length=4, validators=[django.core.validators.RegexValidator(message='Debe estar formado por 3 o 4 dígitos.', regex='^\\d{3,4}$')]),
        ),
        migrations.AddField(
            model_name='program',
            name='passes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='program',
            name='specific_objectives',
            field=models.TextField(blank=True, null=True, verbose_name='Objetivos Específicos'),
        ),
        migrations.AddField(
            model_name='program',
            name='validity_date_d',
            field=models.IntegerField(blank=True, null=True, validators=[pdfapp.validators.validate_days_month], verbose_name='Día'),
        ),
        migrations.AddField(
            model_name='program',
            name='validity_date_m',
            field=models.IntegerField(blank=True, choices=[(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')], null=True, verbose_name='Mes'),
        ),
        migrations.AddField(
            model_name='program',
            name='validity_date_y',
            field=models.IntegerField(blank=True, null=True, validators=[pdfapp.validators.validate_program_years], verbose_name='Año'),
        ),
        migrations.AlterField(
            model_name='program',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pdfapp.Code'),
        ),
        migrations.AlterField(
            model_name='program',
            name='objectives',
            field=models.TextField(blank=True, null=True, verbose_name='Objetivos Generales'),
        ),
        migrations.RemoveField(
            model_name='program',
            name='recommended_sources',
        ),
        migrations.AlterField(
            model_name='program',
            name='validity_trimester',
            field=models.CharField(blank=True, choices=[('1: ene-mar', 'Enero-Marzo'), ('2: abr-jul', 'Abril-Julio'), ('3: jul-ago', 'Julio-Agosto (Intensivo)'), ('4: sep-dic', 'Septiembre-Diciembre')], max_length=10, null=True, verbose_name='Trimestre propuesto'),
        ),
        migrations.AlterField(
            model_name='program',
            name='validity_year',
            field=models.IntegerField(blank=True, null=True, validators=[pdfapp.validators.validate_program_years], verbose_name='Año propuesto'),
        ),
        migrations.AddField(
            model_name='additionalfield',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pdfapp.AdditionalName'),
        ),
        migrations.AddField(
            model_name='program',
            name='additional_fields',
            field=models.ManyToManyField(blank=True, to='pdfapp.AdditionalField'),
        ),
        migrations.AddField(
            model_name='program',
            name='recommended_sources',
            field=models.ManyToManyField(blank=True, to='pdfapp.Reference'),
        ),
    ]
