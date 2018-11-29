# Generated by Django 2.1.3 on 2018-11-27 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20181127_0429'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('description', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='FileFolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Subjects')),
            ],
        ),
        migrations.RemoveField(
            model_name='files',
            name='subject',
        ),
        migrations.DeleteModel(
            name='Files',
        ),
        migrations.AddField(
            model_name='file',
            name='folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.FileFolder'),
        ),
    ]