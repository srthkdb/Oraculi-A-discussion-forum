# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-12 23:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20181112_2131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussion',
            name='picture',
        ),
    ]