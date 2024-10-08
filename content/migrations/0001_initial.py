# Generated by Django 3.2.4 on 2024-08-25 23:41

import content.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_content', models.CharField(choices=[('image', 'Image'), ('docs', 'Docs'), ('video', 'Video'), ('audio', 'Audio'), ('sticker', 'Sticker')], max_length=10)),
                ('content', models.FileField(upload_to=content.models.content_upload_path)),
                ('extention', models.CharField(blank=True, max_length=50, null=True)),
                ('duration', models.CharField(blank=True, max_length=10, null=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=content.models.thumbnail_upload_path)),
                ('channel_type', models.CharField(choices=[('blackhall', 'Blackhall')], max_length=10)),
                ('uploader', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
