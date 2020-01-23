# Generated by Django 3.0.2 on 2020-01-23 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Drivers_Selection', '0018_auto_20200123_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='habit',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='driver',
            name='available_seats',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='driver',
            name='fuel_consumption',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='driver',
            name='fuel_type',
            field=models.CharField(default='', max_length=2),
        ),
    ]
