# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailuser',
            name='quota',
            field=models.IntegerField(default=512, help_text=b'Quota in MB'),
        ),
    ]
