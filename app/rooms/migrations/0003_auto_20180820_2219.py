# Generated by Django 2.1 on 2018-08-20 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_roomreservation_reserved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomreservation',
            name='reserved',
            field=models.DateField(blank=True, null=True, verbose_name='예약된 날짜'),
        ),
    ]