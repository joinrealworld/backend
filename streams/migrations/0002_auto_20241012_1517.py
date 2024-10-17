# Generated by Django 3.2.4 on 2024-10-12 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stream',
            name='url',
        ),
        migrations.AddField(
            model_name='stream',
            name='end_time',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='stream',
            name='server_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='stream',
            name='start_time',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='stream',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
