# Generated by Django 3.2.16 on 2023-01-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_moduleinstallationexecution'),
    ]

    operations = [
        migrations.AddField(
            model_name='backupmodule',
            name='module_config',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='storagemodule',
            name='module_config',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]
