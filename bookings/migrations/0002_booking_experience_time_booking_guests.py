# Generated by Django 4.2 on 2023-04-21 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='experience_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='guests',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
