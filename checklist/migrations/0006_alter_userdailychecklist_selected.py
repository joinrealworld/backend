# Generated by Django 3.2.4 on 2024-04-30 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0005_auto_20240430_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdailychecklist',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]
