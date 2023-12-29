# Generated by Django 5.0 on 2023-12-26 17:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_crud', '0006_passengerseat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passengerdetails',
            name='route',
        ),
        migrations.AddField(
            model_name='passengerdetails',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend_crud.schedule'),
        ),
    ]