# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 03:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdfapp', '0022_auto_20170312_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pdfapp.Code'),
        ),
    ]
