# Generated by Django 5.1.3 on 2024-11-20 09:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_alter_invitetoproject_expire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitetoproject',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 11, 27, 9, 9, 34, 508363, tzinfo=datetime.timezone.utc)),
        ),
    ]
