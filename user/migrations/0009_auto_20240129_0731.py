# Generated by Django 3.2.4 on 2024-01-29 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_accesstokenlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sound_effect',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='theme',
            field=models.CharField(choices=[('dark', 'Dark'), ('light', 'Light')], default='dark', max_length=20),
        ),
    ]