# Generated by Django 3.2.16 on 2022-11-23 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20221123_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='storageexecution',
            name='errors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='storageexecution',
            name='logs',
            field=models.TextField(blank=True, null=True),
        ),
    ]
