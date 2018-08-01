from django.conf import settings
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from .facilities import Facilities

__all__ = (
    'Rooms',
    'RoomDetail',
    'RoomImage',
)


class Rooms(models.Model):
    # 호스트가 없으면 숙소 계약이 성립되지 않음, 회원탈퇴하면 글도 지워지도록,
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='with_host',
    )

    # 숙소 이름
    rooms_name = models.CharField(max_length=50)

    tag = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.rooms_name


class RoomDetail(models.Model):
    """
    Rooms Details 세부 사항,
    """
    ROOMS_TYPE_APARTMENT = 'AP'
    ROOMS_TYPE_HOUSING = 'HO'
    ROOMS_TYPE_ONEROOM = 'OR'
    ROOMS_TYPE_GUESTHOUSE = 'GH'

    ROOMS_TYPE = (
        (ROOMS_TYPE_APARTMENT, '아파트'),
        (ROOMS_TYPE_HOUSING, '주택'),
        (ROOMS_TYPE_ONEROOM, '원룸'),
        (ROOMS_TYPE_GUESTHOUSE, '게스트하우스'),
    )

    rooms = models.ForeignKey(
        Rooms,
        on_delete=models.CASCADE,
        related_name='with_rooms'
    )

    # 숙소 설명
    rooms_description = models.CharField(max_length=200)

    # 객실 수
    rooms_amount = models.PositiveSmallIntegerField()

    # 침대 갯수
    rooms_bed = models.PositiveSmallIntegerField()

    # 숙박 인원
    rooms_personnel = models.PositiveSmallIntegerField()

    # 욕실 갯수
    rooms_bathroom = models.PositiveSmallIntegerField()

    # 숙소 유형
    rooms_type = models.CharField(choices=ROOMS_TYPE, max_length=2, default=ROOMS_TYPE_ONEROOM)

    # 편의 시설
    rooms_facilities = models.ManyToManyField(
        Facilities,
        related_name='rooms_facilities',
        blank=True,
    )

    # 체크인 최소
    check_in_minimum = models.PositiveSmallIntegerField(default=1)

    # 체크인 최대
    check_in_maximum = models.PositiveSmallIntegerField(default=3)

    # 일일 요금
    days_price = models.PositiveIntegerField()

    # 환불규정
    refund = models.TextField()

    # 나라
    address_country = models.CharField(max_length=100)

    # 도시
    address_city = models.CharField(max_length=50)

    # 시/군/구
    address_district01 = models.CharField(max_length=100)

    # 동/읍/면
    address_district02 = models.CharField(max_length=100)

    # 상세주소
    address_detail = models.CharField(max_length=100)

    # 위도
    address_latitude = models.DecimalField(
        decimal_places=14,
        max_digits=16,
    )

    # 경도
    address_longitude = models.DecimalField(
        decimal_places=14,
        max_digits=17,
    )

    # 생성 일자 자동 저장
    created_at = models.DateField(auto_now_add=True)

    # 수정 일자 자동 저장
    modified_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.pk} {self.rooms.rooms_name}'


class RoomImage(models.Model):
    """
    Room Cover image
    """
    room = models.ForeignKey(
        RoomDetail,
        on_delete=models.CASCADE,
        related_name='room_images',
    )

    image_cover = models.ImageField(
        upload_to='room_image_cover',
        blank=True,
    )

    image_cover_thumbnail = ImageSpecField(
        source='image_cover',
        processors=[ResizeToFill(308, 206)],
        format='PNG',
        options={'quality': 100},
    )


class RoomRules(models.Model):
    room = models.ForeignKey(
        RoomDetail,
        on_delete=models.CASCADE,
        related_name='room_rules'
    )
    rule_list = models.CharField(max_length=50)
