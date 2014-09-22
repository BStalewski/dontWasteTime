# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('link', models.URLField()),
                ('desc', models.TextField()),
                ('price', models.IntegerField()),
                ('time_posted', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
