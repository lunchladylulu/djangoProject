# Generated by Django 3.2.16 on 2023-01-20 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_auto_20230120_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='itinerary',
            name='day_3',
            field=models.CharField(default='default', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itinerary',
            name='day_4',
            field=models.CharField(default='default', max_length=200),
            preserve_default=False,
        ),
    ]
