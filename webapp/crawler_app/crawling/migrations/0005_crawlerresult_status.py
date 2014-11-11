# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0004_crawlerresult_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawlerresult',
            name='status',
            field=models.CharField(default='NEW', max_length=5, choices=[('NEW', 'new'), ('ACC', 'accepted'), ('IGN', 'ignored')]),
            preserve_default=True,
        ),
    ]
