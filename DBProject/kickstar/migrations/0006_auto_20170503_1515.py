# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-03 15:15
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kickstar', '0005_usercreditcardinfo_creditname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectpropose',
            name='pcontentdetail',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
