# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-21 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cerbereapp', '0004_auto_20160520_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentmodel',
            name='profiles',
            field=models.ManyToManyField(to='cerbereapp.Profile'),
        ),
    ]
