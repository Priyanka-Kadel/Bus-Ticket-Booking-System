# Generated by Django 5.0 on 2023-12-21 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_crud', '0003_remove_route_stop_bus_total_seat_schedule_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='busseatstatus',
            name='seat_side',
            field=models.CharField(choices=[('A', 'Side A'), ('B', 'Side B')], default='A', max_length=1),
        ),
    ]
