# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-11 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userextend',
            name='company',
            field=models.ManyToManyField(related_name='user_extend', to='theme.Company'),
        ),
    ]
