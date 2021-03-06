# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 16:04
from __future__ import unicode_literals

from django.db import migrations, models
import pdfapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pdfapp', '0034_auto_20170317_1148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['first_surname', 'first_name']},
        ),
        migrations.AlterField(
            model_name='program',
            name='credits',
            field=models.IntegerField(blank=True, null=True, validators=[pdfapp.validators.validate_credits], verbose_name='Unidad de Créditos'),
        ),
        migrations.AlterField(
            model_name='program',
            name='laboratory_hours',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[pdfapp.validators.validate_positive_integer, pdfapp.validators.validate_max_hours], verbose_name='Horas de Laboratorio'),
        ),
        migrations.AlterField(
            model_name='program',
            name='practice_hours',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[pdfapp.validators.validate_positive_integer, pdfapp.validators.validate_max_hours], verbose_name='Horas de Práctica'),
        ),
        migrations.AlterField(
            model_name='program',
            name='theory_hours',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[pdfapp.validators.validate_positive_integer, pdfapp.validators.validate_max_hours], verbose_name='Horas de Teoría'),
        ),
        migrations.AlterField(
            model_name='program',
            name='validity_date_d',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[pdfapp.validators.validate_days_month], verbose_name='Día'),
        ),
    ]
