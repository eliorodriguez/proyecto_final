# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-10 22:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exploration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shapes',
            name='size',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]
