# Generated by Django 3.2.16 on 2023-01-20 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_itinerary_identifier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itinerary',
            name='identifier',
        ),
    ]
