# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-04 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kickstar', '0009_auto_20170503_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='interests',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
