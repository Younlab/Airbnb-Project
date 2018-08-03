# Generated by Django 2.1 on 2018-08-03 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='address_city',
            field=models.CharField(help_text='도시', max_length=50),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='address_country',
            field=models.CharField(help_text='국가', max_length=30),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='address_detail',
            field=models.CharField(help_text='상세 주소', max_length=100),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='address_district01',
            field=models.CharField(help_text='시/군/구', max_length=100),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='address_district02',
            field=models.CharField(help_text='동/읍/면', max_length=100),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='address_latitude',
            field=models.DecimalField(decimal_places=14, help_text='Google MAP API 위도', max_digits=16),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='address_longitude',
            field=models.DecimalField(decimal_places=14, help_text='Google MAP API 경도', max_digits=17),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='rooms_description',
            field=models.TextField(help_text='당신의 숙소를 소개하세요, 게스트의 흥미를 유발하는것이 중요합니다.', max_length=200),
        ),
    ]
