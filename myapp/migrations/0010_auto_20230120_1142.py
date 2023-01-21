# Generated by Django 3.2.16 on 2023-01-20 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.IntegerField()),
                ('city', models.CharField(max_length=50)),
                ('time_of_day', models.CharField(max_length=50)),
                ('activity_type', models.CharField(max_length=50)),
                ('day_1', models.CharField(max_length=300)),
                ('day_2', models.CharField(max_length=300)),
                ('day_3', models.CharField(max_length=300)),
                ('day_4', models.CharField(max_length=300)),
            ],
        ),
        migrations.DeleteModel(
            name='Length',
        ),
    ]
