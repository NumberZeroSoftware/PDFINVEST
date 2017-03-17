# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-16 16:41
from __future__ import unicode_literals

from django.db import migrations, models
import pdfapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pdfapp', '0025_auto_20170315_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='validity_date_d',
            field=models.IntegerField(default=1, validators=[pdfapp.validators.validate_days_month], verbose_name='Día'),
        ),
    ]