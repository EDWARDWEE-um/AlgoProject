# Generated by Django 3.2.4 on 2021-06-08 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_distance_distanceshortest'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='oriToDes',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
