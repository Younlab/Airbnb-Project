from django.conf import settings
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

__all__ = (
    'Rooms',
    'RoomRules',
    'RoomImageList',
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
        max_length=50,
    )

    # 호스트
    rooms_host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='호스트',
        help_text='숙소의 오너입니다.',
        on_delete=models.CASCADE,
        related_name='with_host_rooms',
    )

    # 커버 이미지
    image_cover = models.ImageField(
        verbose_name='커버 이미지',
        help_text='게스트에게 소개할 숙소의 커버 이미지를 업로드 해 주세요',
        upload_to='room_image_cover',
        blank=True,
    )

    # 썸네일 이미지, form 사용시 랜더링되지 않음
    image_cover_thumbnail = ImageSpecField(
        source='image_cover',
        processors=[ResizeToFill(308, 206)],
        format='PNG',
        options={'quality': 100},
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
    )

    # 환불규정
    refund = models.TextField(
        verbose_name='환불 규정',
        help_text='환불 규정을 가급적 상세히 입력해주세요'
    )

    # 나라
    address_country = models.CharField(
        verbose_name='국가',
        max_length=30,
    )

    # 도시
    address_city = models.CharField(
        verbose_name='도시',
        max_length=50,
    )

    # 시/군/구
    address_district01 = models.CharField(
        verbose_name='시/군/구',
        max_length=100,
    )

    # 동/읍/면
    address_district02 = models.CharField(
        verbose_name='동/읍/면',
        max_length=100,
    )

    # 상세주소
    address_detail = models.CharField(
        verbose_name='상세 주소',
        max_length=100,
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
    room = models.ForeignKey(
        Rooms,
        on_delete=models.CASCADE,
        related_name='room_rules'
    )
    rule_list = models.CharField(max_length=50)


class RoomImageList(models.Model):
    """
    이미지 리스트
    """
    room = models.ForeignKey(
        Rooms,
        on_delete=models.CASCADE,
        related_name='room_image_lists'
    )
    room_image_list = models.ImageField(
        upload_to='room_image_list'
    )

    def __str__(self):
        return self.room_image_list


class RoomFacilities(models.Model):
    """
    편의시설 리스트
    """
    room = models.ForeignKey(
        Rooms,
        on_delete=models.CASCADE,
        related_name='room_facilities'
    )

    facilities = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.facilities
