# Generated by Django 3.2.4 on 2024-05-31 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0028_user_identity_booster'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='selected_emoji',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
