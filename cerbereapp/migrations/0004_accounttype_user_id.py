# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-15 13:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cerbereapp', '0003_accounttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttype',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
