# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 04:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdfapp', '0031_auto_20170317_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='programa',
            name='creditos',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Créditos'),
        ),
    ]
