# Generated by Django 3.0.2 on 2020-01-23 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Drivers_Selection', '0019_auto_20200123_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passenger',
            name='destination_place',
        ),
    ]
