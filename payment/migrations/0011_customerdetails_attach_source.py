# Generated by Django 3.2.4 on 2024-04-12 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_customerdetails_card_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerdetails',
            name='attach_source',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
