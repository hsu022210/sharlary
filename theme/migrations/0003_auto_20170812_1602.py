# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-12 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0002_auto_20170811_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
