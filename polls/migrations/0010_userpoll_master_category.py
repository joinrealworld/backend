# Generated by Django 3.2.4 on 2024-06-16 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0014_mastercategory_category_pic2'),
        ('polls', '0009_usercheckedlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpoll',
            name='master_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='channel.mastercategory'),
        ),
    ]
