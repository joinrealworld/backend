# Generated by Django 3.2.4 on 2024-01-24 01:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0002_coursequiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='coursequiz',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='courses',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
