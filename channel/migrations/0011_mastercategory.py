# Generated by Django 3.2.4 on 2024-04-12 18:46

import channel.models
import ckeditor.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0010_completecontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=128)),
                ('category_pic', models.ImageField(blank=True, null=True, upload_to=channel.models.master_category_pic_path)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
            ],
        ),
    ]
