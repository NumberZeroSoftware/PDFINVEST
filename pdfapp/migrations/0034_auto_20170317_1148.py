# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdfapp', '0033_merge_20170317_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='passes',
            field=models.BooleanField(default=False, verbose_name='Enviar para aprobar'),
        ),
        migrations.AlterField(
            model_name='programa',
            name='codigo',
            field=models.CharField(max_length=6, verbose_name='Código'),
        ),
    ]
