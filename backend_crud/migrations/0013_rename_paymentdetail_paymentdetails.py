# Generated by Django 5.0 on 2024-01-07 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend_crud', '0012_paymentdetail'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PaymentDetail',
            new_name='PaymentDetails',
        ),
    ]
