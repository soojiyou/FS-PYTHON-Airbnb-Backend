# Generated by Django 4.2 on 2023-04-21 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_booking_experience_time_booking_guests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='guests',
            field=models.PositiveIntegerField(),
        ),
    ]