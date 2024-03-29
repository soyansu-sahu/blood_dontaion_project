# Generated by Django 4.0.6 on 2022-07-30 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodGroupSessionMapper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloodgroups', to='myapp.bloodgroup')),
                ('request_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='myapp.bloodrequestsession')),
            ],
        ),
    ]
