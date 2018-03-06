# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-22 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exploration', '0006_auto_20180221_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='BinaryRelations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('axe', models.CharField(max_length=1)),
                ('name', models.CharField(max_length=10)),
                ('value', models.DecimalField(decimal_places=5, max_digits=8)),
                ('part_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='part_one', to='exploration.Parts')),
                ('part_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='part_two', to='exploration.Parts')),
            ],
        ),
    ]
