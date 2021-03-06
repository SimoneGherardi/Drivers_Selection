# Generated by Django 3.0.2 on 2020-01-23 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Drivers_Selection', '0015_auto_20200123_1149'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RankElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_in_rank', models.IntegerField(default=0)),
                ('id_element', models.IntegerField(default=0)),
                ('score', models.FloatField(default=0)),
                ('rank', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Drivers_Selection.Rank')),
            ],
        ),
        migrations.DeleteModel(
            name='Ranking',
        ),
    ]
