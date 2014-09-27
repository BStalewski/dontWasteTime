# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0003_auto_20140922_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawlerresult',
            name='source',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
    ]
