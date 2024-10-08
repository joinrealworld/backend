# Generated by Django 3.2.4 on 2024-10-08 23:33

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
            name='Clan',
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
            model_name='clan',
            index=models.Index(fields=['timestamp'], name='clan_clan_timesta_24ef50_idx'),
        ),
        migrations.AddIndex(
            model_name='clan',
            index=models.Index(fields=['user'], name='clan_clan_user_id_21c98d_idx'),
        ),
    ]
