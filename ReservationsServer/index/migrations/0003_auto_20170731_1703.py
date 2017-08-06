# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_auto_20170731_1701'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performancedate',
            old_name='noMoreSeats',
            new_name='noMoreFreeSeats',
        ),
    ]
