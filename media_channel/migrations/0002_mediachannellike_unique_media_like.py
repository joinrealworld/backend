# Generated by Django 3.2.4 on 2024-08-26 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_channel', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='mediachannellike',
            constraint=models.UniqueConstraint(fields=('media_channel', 'user'), name='unique_media_like'),
        ),
    ]
