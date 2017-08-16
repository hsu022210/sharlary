# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-16 16:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=300)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('salary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='theme.Salary')),
                ('user_extend', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='theme.UserExtend')),
            ],
        ),
    ]