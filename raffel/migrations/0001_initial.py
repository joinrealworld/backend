# Generated by Django 3.2.4 on 2024-10-11 06:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Raffel',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='raffel',
            index=models.Index(fields=['timestamp'], name='raffel_raff_timesta_79928b_idx'),
        ),
        migrations.AddIndex(
            model_name='raffel',
            index=models.Index(fields=['user'], name='raffel_raff_user_id_91773f_idx'),
        ),
    ]
