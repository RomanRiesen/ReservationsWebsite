# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-20 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reservation_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservation',
            name='reservation_hash',
            field=models.CharField(default='', max_length=255),
        ),
    ]
