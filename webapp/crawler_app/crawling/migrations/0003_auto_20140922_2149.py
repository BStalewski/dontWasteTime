# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0002_auto_20140922_2141'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CrawlerItem',
            new_name='CrawlerResult',
        ),
    ]
