# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 22:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdfapp', '0020_auto_20170225_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='document',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdfapp.Document'),
        ),
    ]