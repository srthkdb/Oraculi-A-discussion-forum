# Generated by Django 2.1.3 on 2018-11-27 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20181127_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='favourite',
            field=models.BooleanField(default=False),
        ),
    ]
