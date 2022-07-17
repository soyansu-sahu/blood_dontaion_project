# Generated by Django 4.0.6 on 2022-07-17 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodGroup',
            fields=[
                ('name', models.CharField(max_length=4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='BloodGroupSessionMapper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloodgroups', to='myapp.bloodgroup')),
            ],
        ),
        migrations.CreateModel(
            name='BloodRequestSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pincode', models.IntegerField()),
                ('total_unit', models.PositiveIntegerField(default=1)),
                ('req_date', models.DateTimeField(default=django.utils.timezone.now, max_length=100)),
                ('till_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('blood_groups', models.ManyToManyField(related_name='requests', through='myapp.BloodGroupSessionMapper', to='myapp.bloodgroup')),
                ('req_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('contact_no', models.CharField(max_length=10, unique=True)),
                ('pincode', models.IntegerField()),
                ('image', models.ImageField(blank=True, upload_to='static/images')),
                ('is_donor', models.BooleanField(default=True)),
                ('last_donated_date', models.DateField(blank=True, null=True)),
                ('blood_group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='myapp.bloodgroup')),
            ],
        ),
        migrations.CreateModel(
            name='BloodRequestStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invitation_status', models.CharField(default='PENDING', max_length=10)),
                ('donation_status', models.BooleanField(default=False)),
                ('donation_date', models.DateField(blank=True, null=True)),
                ('blood_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloodgroup', to='myapp.bloodgroup')),
                ('donner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.bloodrequestsession')),
            ],
        ),
        migrations.AddField(
            model_name='bloodgroupsessionmapper',
            name='request_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='myapp.bloodrequestsession'),
        ),
    ]
