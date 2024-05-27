# Generated by Django 3.2.4 on 2024-04-27 21:37

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_delete_userwallpaper'),
    ]

    operations = [
        migrations.CreateModel(
            name='WallPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallpaper', models.ImageField(blank=True, null=True, upload_to=user.models.wallpaper_path)),
                ('price', models.PositiveIntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]