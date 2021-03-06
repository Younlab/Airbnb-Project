from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationReserved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disable_days', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomFacilities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facilities', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_image', models.ImageField(max_length=255, upload_to='room_profile_image',
                                                 verbose_name='숙소 프로필 이미지를 업로드 해주세요')),
            ],
        ),
        migrations.CreateModel(
            name='RoomReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_personnel', models.PositiveSmallIntegerField(verbose_name='숙박 인원')),
                ('checkin', models.DateField(blank=True, verbose_name='체크인 날짜')),
                ('checkout', models.DateField(blank=True, verbose_name='체크아웃 날짜')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('guest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                            to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RoomRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_list', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rooms_name', models.CharField(help_text='숙소의 이름을 입력하세요', max_length=150, verbose_name='숙소 이름')),
                ('rooms_tag',
                 models.CharField(blank=True, help_text='검색에 사용될 지역 태그를 입력하세요', max_length=150, verbose_name='태그')),
                ('rooms_cover_image',
                 models.ImageField(max_length=255, upload_to='cover_image', verbose_name='숙소의 커버 이미지입니다.')),
                ('days_price', models.PositiveIntegerField(help_text='일일 숙박 요금을 입력하세요', verbose_name='일일 숙박 요금')),
                ('rooms_description',
                 models.TextField(help_text='당신의 숙소를 소개하세요, 게스트의 흥미를 유발하는것이 중요합니다.', max_length=255,
                                  verbose_name='숙소 개요')),
                ('rooms_amount', models.PositiveSmallIntegerField(help_text='숙소 내의 객실 수를 입력하세요', verbose_name='객실 수')),
                ('rooms_bed', models.PositiveSmallIntegerField(help_text='객실 내의 침대 수를 입력하세요', verbose_name='침대 수')),
                ('rooms_personnel',
                 models.PositiveSmallIntegerField(help_text='최대 숙박 가능인원을 입력하세요', verbose_name='숙박 가능 인원')),
                (
                'rooms_bathroom', models.PositiveSmallIntegerField(help_text='숙소 내의 욕실 수를 입력하세요', verbose_name='욕실 수')),
                ('rooms_type',
                 models.CharField(choices=[('AP', '아파트'), ('HO', '주택'), ('OR', '원룸'), ('GH', '게스트하우스')], default='OR',
                                  help_text='숙소의 유형을 선택해주세요', max_length=2, verbose_name='숙소 유형')),
                ('check_in_minimum', models.PositiveSmallIntegerField(default=1, help_text='최소 숙박 가능일 수를 입력해주세요',
                                                                      verbose_name='최소 숙박 가능일')),
                ('check_in_maximum',
                 models.PositiveSmallIntegerField(blank=True, default=3, help_text='최대 숙박 가능일 수를 입력해주세요',
                                                  verbose_name='최대 숙박 가능일')),
                ('refund', models.TextField(blank=True,
                                            default='\n                일반 정책 \n\n                More information \n\n                체크인 5일 전까지 예약을 취소하면 에어비앤비 서비스 수수료을 제외한 요금이 환불됩니다.\n\n                체크인까지 5일이 남지 않은 시점에 예약을 취소하면 첫 1박 요금과 나머지 숙박 요금의 50%는 환불되지 않습니다. \n\n                에어비앤비 서비스 수수료는 예약 후 48시간 이내에 취소하고 체크인 전인 경우에만 환불됩니다. \n\n                ',
                                            help_text='환불 규정을 가급적 상세히 입력해주세요', verbose_name='환불 규정')),
                ('address_country', models.CharField(blank=True, max_length=50, verbose_name='국가')),
                ('address_city', models.CharField(blank=True, max_length=100, verbose_name='도시')),
                ('address_district', models.CharField(blank=True, max_length=150, verbose_name='시/군/구')),
                ('address_detail', models.CharField(blank=True, max_length=150, verbose_name='상세 주소')),
                ('address_latitude',
                 models.DecimalField(blank=True, decimal_places=14, max_digits=16, verbose_name='Google MAP API 위도')),
                ('address_longitude',
                 models.DecimalField(blank=True, decimal_places=14, max_digits=17, verbose_name='Google MAP API 경도')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('rooms_host', models.ForeignKey(help_text='숙소의 오너입니다.', on_delete=django.db.models.deletion.CASCADE,
                                                 related_name='with_host_rooms', to=settings.AUTH_USER_MODEL,
                                                 verbose_name='호스트')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='roomrules',
            name='room',
            field=models.ManyToManyField(blank=True, related_name='room_rules', to='rooms.Rooms'),
        ),
        migrations.AddField(
            model_name='roomreservation',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_reservations',
                                    to='rooms.Rooms'),
        ),
        migrations.AddField(
            model_name='roomimage',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_images',
                                    to='rooms.Rooms'),
        ),
        migrations.AddField(
            model_name='roomfacilities',
            name='room',
            field=models.ManyToManyField(related_name='room_facilities', to='rooms.Rooms'),
        ),
        migrations.AddField(
            model_name='reservationreserved',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations_disable',
                                    to='rooms.RoomReservation'),
        ),
    ]
