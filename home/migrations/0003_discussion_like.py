# Generated by Django 2.1.2 on 2018-10-20 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_discussion_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='like',
            field=models.BooleanField(default=False),
        ),
    ]
