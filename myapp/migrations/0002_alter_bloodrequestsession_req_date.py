# Generated by Django 4.0.6 on 2022-07-17 12:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodrequestsession',
            name='req_date',
            field=models.DateTimeField(default=datetime.datetime.utcnow, max_length=100),
        ),
    ]