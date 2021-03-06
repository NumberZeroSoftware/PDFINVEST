# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-25 00:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdfapp', '0010_auto_20170223_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='code',
            field=models.CharField(max_length=10, verbose_name='Código'),
        ),
        migrations.AlterField(
            model_name='program',
            name='coordination',
            field=models.ManyToManyField(blank=True, to='pdfapp.Coordination', verbose_name='Coordinación'),
        ),
        migrations.AlterField(
            model_name='program',
            name='credits',
            field=models.IntegerField(blank=True, null=True, verbose_name='Unidad de Créditos'),
        ),
        migrations.AlterField(
            model_name='program',
            name='denomination',
            field=models.CharField(max_length=60, verbose_name='Denominación'),
        ),
        migrations.AlterField(
            model_name='program',
            name='evaluation_strategies',
            field=models.TextField(blank=True, verbose_name='Estrategias de Evaluación'),
        ),
        migrations.AlterField(
            model_name='program',
            name='laboratory_hours',
            field=models.IntegerField(blank=True, null=True, verbose_name='Horas de Laboratorio'),
        ),
        migrations.AlterField(
            model_name='program',
            name='methodological_strategies',
            field=models.TextField(blank=True, verbose_name='Estrategias Metodológicas'),
        ),
        migrations.AlterField(
            model_name='program',
            name='practice_hours',
            field=models.IntegerField(blank=True, null=True, verbose_name='Horas de Práctica'),
        ),
        migrations.AlterField(
            model_name='program',
            name='recommended_sources',
            field=models.TextField(blank=True, verbose_name='Fuentes de Información Recomendadas'),
        ),
        migrations.AlterField(
            model_name='program',
            name='requirements',
            field=models.TextField(blank=True, verbose_name='Requisitos'),
        ),
        migrations.AlterField(
            model_name='program',
            name='synoptic_content',
            field=models.TextField(blank=True, verbose_name='Contenidos Sipnóticos'),
        ),
        migrations.AlterField(
            model_name='program',
            name='theory_hours',
            field=models.IntegerField(blank=True, null=True, verbose_name='Horas de Teoría'),
        ),
    ]
