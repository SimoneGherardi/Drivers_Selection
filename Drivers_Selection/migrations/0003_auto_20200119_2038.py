# Generated by Django 3.0.2 on 2020-01-19 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Drivers_Selection', '0002_auto_20200119_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='car_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='driver',
            name='fuel_type',
            field=models.CharField(default='', max_length=50),
        ),
    ]
