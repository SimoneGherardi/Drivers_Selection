# Generated by Django 3.0.2 on 2020-01-19 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Drivers_Selection', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passenger',
            name='starting_point',
        ),
        migrations.AddField(
            model_name='passenger',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='passenger',
            name='city',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='passenger',
            name='country_code',
            field=models.CharField(default='', max_length=2),
        ),
        migrations.AddField(
            model_name='passenger',
            name='zip_code',
            field=models.CharField(default='', max_length=20),
        ),
    ]
