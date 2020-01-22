# Generated by Django 3.0.2 on 2020-01-18 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_name', models.CharField(max_length=50)),
                ('fuel_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(default='', max_length=100)),
                ('country_code', models.CharField(default='', max_length=2)),
                ('zip_code', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Drivers_Selection.Person')),
                ('starting_point', models.CharField(default='', max_length=200)),
            ],
            bases=('Drivers_Selection.person',),
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('passenger_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Drivers_Selection.Passenger')),
            ],
            bases=('Drivers_Selection.passenger',),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passengers', models.ManyToManyField(related_name='not_driving_passengers', to='Drivers_Selection.Passenger')),
                ('drivers', models.ManyToManyField(related_name='driving_passengers', to='Drivers_Selection.Driver')),
            ],
        ),
    ]
