# Generated by Django 2.0.7 on 2018-08-01 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Facilities', models.CharField(max_length=400)),
                ('room_info', models.TextField()),
                ('rule', models.TextField()),
                ('price', models.IntegerField()),
                ('location', models.CharField(max_length=200)),
            ],
        ),
    ]
