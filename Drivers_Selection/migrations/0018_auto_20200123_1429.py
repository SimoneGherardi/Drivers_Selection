# Generated by Django 3.0.2 on 2020-01-23 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Drivers_Selection', '0017_auto_20200123_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rank',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
