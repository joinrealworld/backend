# Generated by Django 3.2.4 on 2024-04-30 23:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0004_userdailychecklist_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='masterchecklist',
            name='data',
        ),
        migrations.RemoveField(
            model_name='userdailychecklist',
            name='data',
        ),
        migrations.AddField(
            model_name='masterchecklist',
            name='checklist',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='masterchecklist',
            name='copied_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='userdailychecklist',
            name='master_checklist',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='checklist.masterchecklist'),
            preserve_default=False,
        ),
    ]
