# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-11 03:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exploration', '0003_parts_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitRelations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('axe', models.CharField(max_length=1)),
                ('value', models.DecimalField(decimal_places=3, max_digits=8)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exploration.Parts')),
            ],
        ),
    ]
