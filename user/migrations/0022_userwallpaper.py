# Generated by Django 3.2.4 on 2024-04-27 21:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_wallpaper'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWallPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_purchase', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wallpaper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.wallpaper')),
            ],
        ),
    ]