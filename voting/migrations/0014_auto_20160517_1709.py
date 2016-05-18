# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 21:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0013_auto_20141003_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='restrict_to',
            field=models.ManyToManyField(blank=True, to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='viewers',
            field=models.ManyToManyField(blank=True, related_name='view_only_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
