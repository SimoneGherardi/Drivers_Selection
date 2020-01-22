# Generated by Django 3.0.2 on 2020-01-22 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Drivers_Selection', '0012_place_is_valid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='passenger',
            name='destination_place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='destination_place', to='Drivers_Selection.Place'),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='starting_place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='starting_place', to='Drivers_Selection.Place'),
        ),
        migrations.AlterField(
            model_name='place',
            name='is_destination',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField(default=0)),
                ('col', models.IntegerField(default=0)),
                ('val', models.FloatField(default=0)),
                ('matrix', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Drivers_Selection.Matrix')),
            ],
        ),
    ]
