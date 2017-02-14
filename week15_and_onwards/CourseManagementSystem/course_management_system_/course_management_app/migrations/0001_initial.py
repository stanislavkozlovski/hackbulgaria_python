# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 16:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('week', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('url', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_management_app.Course')),
            ],
        ),
    ]