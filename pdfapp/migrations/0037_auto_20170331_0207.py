# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-31 02:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdfapp', '0036_auto_20170331_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='author',
            field=models.ManyToManyField(blank=True, to='pdfapp.Author', verbose_name='Autor'),
        ),
    ]
