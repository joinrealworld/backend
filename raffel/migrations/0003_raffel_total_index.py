# Generated by Django 4.2 on 2024-11-14 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raffel', '0002_raffel_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='raffel',
            name='total_index',
            field=models.PositiveIntegerField(default=1),
        ),
    ]