# Generated by Django 5.0.3 on 2024-03-25 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0003_alter_customers_phone_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers',
            name='phone_no',
        ),
    ]
