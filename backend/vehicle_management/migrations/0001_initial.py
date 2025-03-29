# Generated by Django 5.1.7 on 2025-03-29 06:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('lo', 'level_one'), ('lt', 'level_two'), ('lth', 'level_three')], default='lo', max_length=12)),
                ('detail', models.TextField()),
                ('prize', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('plate_number', models.IntegerField(unique=True)),
                ('color', models.CharField(max_length=50)),
                ('Model', models.CharField(max_length=100)),
                ('sit_number', models.IntegerField(default=0)),
                ('picture', models.ImageField(upload_to='vehicle_management/vehicle_image')),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.branch')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='documentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc', models.FileField(upload_to='vehicle_management/doc')),
                ('did', models.CharField(max_length=100, unique=True)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_doc', to='vehicle_management.vehicle')),
            ],
        ),
    ]
