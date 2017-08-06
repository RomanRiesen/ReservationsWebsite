# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_auto_20170731_1703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performancedate',
            old_name='noMoreFreeSeats',
            new_name='hasFreeSeats',
        ),
    ]
