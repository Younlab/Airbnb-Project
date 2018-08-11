from django.conf import settings
from django.db import models

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import Thumbnail
from pilkit.processors import ResizeToFill

__all__ = (
    'Rooms',
    'RoomRules',
    'RoomImage',
    'RoomFacilities',
)


class Rooms(models.Model):
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

    # 숙소 이름
    rooms_name = models.CharField(
        verbose_name='숙소 이름',
        help_text='숙소의 이름을 입력하세요',
        max_length=70,
    )

    # 태그
    rooms_tag = models.CharField(
        verbose_name='태그',
        help_text='검색에 사용될 지역 태그를 입력하세요',
        max_length=20,
        blank=True,
    )

    # 호스트
    rooms_host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='호스트',
        help_text='숙소의 오너입니다.',
        on_delete=models.CASCADE,
        related_name='with_host_rooms',
    )

    # 숙소 커버 이미지
    rooms_cover_image = models.ImageField(
        upload_to='cover_image',
        verbose_name='숙소의 커버 이미지입니다.',
    )

    # 일일 요금
    days_price = models.PositiveIntegerField(
        verbose_name='일일 숙박 요금',
        help_text='일일 숙박 요금을 입력하세요'
    )

    # 숙소 설명
    rooms_description = models.TextField(
        verbose_name='숙소 개요',
        help_text='당신의 숙소를 소개하세요, 게스트의 흥미를 유발하는것이 중요합니다.',
        max_length=200
    )

    # 객실 수
    rooms_amount = models.PositiveSmallIntegerField(
        verbose_name='객실 수',
        help_text='숙소 내의 객실 수를 입력하세요'
    )

    # 침대 갯수
    rooms_bed = models.PositiveSmallIntegerField(
        verbose_name='침대 수',
        help_text='객실 내의 침대 수를 입력하세요'
    )

    # 숙박 인원
    rooms_personnel = models.PositiveSmallIntegerField(
        verbose_name='숙박 가능 인원',
        help_text='최대 숙박 가능인원을 입력하세요'
    )

    # 욕실 갯수
    rooms_bathroom = models.PositiveSmallIntegerField(
        verbose_name='욕실 수',
        help_text='숙소 내의 욕실 수를 입력하세요'
    )

    # 숙소 유형
    rooms_type = models.CharField(
        verbose_name='숙소 유형',
        help_text='숙소의 유형을 선택해주세요',
        choices=ROOMS_TYPE,
        max_length=2, default=ROOMS_TYPE_ONEROOM
    )

    # 체크인 최소
    check_in_minimum = models.PositiveSmallIntegerField(
        verbose_name='최소 숙박 가능일',
        help_text='최소 숙박 가능일 수를 입력해주세요',
        default=1,
    )

    # 체크인 최대
    check_in_maximum = models.PositiveSmallIntegerField(
        verbose_name='최대 숙박 가능일',
        help_text='최대 숙박 가능일 수를 입력해주세요',
        default=3,
        blank=True,
    )

    # 환불규정
    refund = models.TextField(
        verbose_name='환불 규정',
        help_text='환불 규정을 가급적 상세히 입력해주세요',
        blank=True,
        default='''
                일반 정책 \n
                More information \n
                체크인 5일 전까지 예약을 취소하면 에어비앤비 서비스 수수료을 제외한 요금이 환불됩니다.\n
                체크인까지 5일이 남지 않은 시점에 예약을 취소하면 첫 1박 요금과 나머지 숙박 요금의 50%는 환불되지 않습니다. \n
                에어비앤비 서비스 수수료는 예약 후 48시간 이내에 취소하고 체크인 전인 경우에만 환불됩니다. \n
                '''
    )

    # 나라
    address_country = models.CharField(
        verbose_name='국가',
        max_length=30,
        blank=True
    )

    # 도시
    address_city = models.CharField(
        verbose_name='도시',
        max_length=50,
        blank=True
    )

    # 시/군/구
    address_district = models.CharField(
        verbose_name='시/군/구',
        max_length=150,
        blank=True
    )

    # 상세주소
    address_detail = models.CharField(
        verbose_name='상세 주소',
        max_length=150,
        blank=True
    )

    # 위도
    address_latitude = models.DecimalField(
        verbose_name='Google MAP API 위도',
        decimal_places=14,
        max_digits=16,
    )

    # 경도
    address_longitude = models.DecimalField(
        verbose_name='Google MAP API 경도',
        decimal_places=14,
        max_digits=17,
    )

    # 생성 일자 자동 저장
    created_at = models.DateField(auto_now_add=True)

    # 수정 일자 자동 저장
    modified_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.pk} {self.rooms_host} {self.rooms_name}'


class RoomRules(models.Model):
    """
    숙소 이용 규칙
    """
    room = models.ManyToManyField(
        Rooms,
        related_name='room_rules',
        blank=True
    )
    rule_list = models.CharField(max_length=50)

    def __str__(self):
        return self.rule_list


class RoomImage(models.Model):
    """
    이미지 리스트
    """
    room = models.ForeignKey(
        Rooms,
        related_name='room_images',
        on_delete=models.CASCADE,
    )
    room_image = models.ImageField(
        upload_to='room_profile_image',
        verbose_name='숙소 프로필 이미지를 업로드 해주세요',
    )

    room_image_thumbnail = ImageSpecField(
        source='room_image',
        processors=[ResizeToFill(308, 206)],
        format='png',
        options={'quality': 100},
    )

    def __str__(self):
        return self.room_image


class RoomFacilities(models.Model):
    """
    편의시설 리스트
    """
    room = models.ManyToManyField(
        Rooms,
        related_name='room_facilities'
    )

    facilities = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return self.facilities


class RoomReservation(models.Model):
    """
    예약 등록
    """
    room = models.ManyToManyField(
        Rooms,
        related_name='room_reservations'
    )

    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    checkin = models.DateField(
        blank=True,
        verbose_name='체크인 날짜',
        unique=True,
    )

    checkout = models.DateField(
        blank=True,
        verbose_name='체크아웃 날짜',
        unique=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.guest}, {self.checkin}, {self.checkout}'
