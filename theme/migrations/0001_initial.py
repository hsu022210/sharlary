# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 16:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('website', models.URLField(blank=True, null=True)),
                ('join_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=30)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=50)),
                ('monthly_pay', models.PositiveIntegerField()),
                ('related_expr', models.PositiveSmallIntegerField()),
                ('education', models.CharField(max_length=10)),
                ('school', models.CharField(blank=True, max_length=50, null=True)),
                ('major', models.CharField(blank=True, max_length=50, null=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('other', models.TextField(blank=True, max_length=300, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salary', to='theme.Company')),
            ],
        ),
        migrations.CreateModel(
            name='UserExtend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ManyToManyField(related_name='user_extend', to='theme.Company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_extend', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='salary',
            name='user_extend',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salary', to='theme.UserExtend'),
        ),
    ]