# Generated by Django 5.1.1 on 2024-09-09 18:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_invitetoproject_expire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitetoproject',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 16, 18, 0, 27, 78464, tzinfo=datetime.timezone.utc)),
        ),
    ]