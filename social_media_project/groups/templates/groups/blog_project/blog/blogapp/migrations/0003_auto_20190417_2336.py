# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-04-18 03:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_auto_20190417_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 18, 3, 36, 57, 820161, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 18, 3, 36, 57, 819254, tzinfo=utc)),
        ),
    ]
