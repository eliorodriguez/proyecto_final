# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-23 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exploration', '0008_auto_20180223_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parts',
            name='axe_x',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=8),
        ),
    ]
