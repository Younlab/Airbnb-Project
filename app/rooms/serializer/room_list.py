from datetime import timedelta

from django.conf import settings
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404

from members.serializers.user import UserSerializer
from ..models.rooms import RoomReservation, RoomFacilities, RoomRules, RoomImage
from ..models import Rooms


class RoomImageSerializer(serializers.ModelSerializer):
    room_image = serializers.ImageField()

    class Meta:
        model = RoomImage
        fields = (
            'room_image',
        )


class RoomListSerializer(serializers.ModelSerializer):
    rooms_cover_thumbnail = serializers.ImageField()

    class Meta:
        model = Rooms
        fields = (
            'pk',
            'rooms_host',
            'rooms_type',
            'rooms_name',
            'rooms_tag',
            'days_price',
            'rooms_cover_thumbnail',
            'created_at',
        )


class RoomReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReservation
        fields = '__all__'

    def validate(self, value):
        if self.initial_data.get('room'):
            # room_pk = self.room.get('pk')
            room_pk = self.initial_data.get('room')
            room = get_object_or_404(Rooms, pk=room_pk)
            value['room'] = room
        else:
            raise serializers.ValidationError('rooms 정보가 전달되지 않았습니다.')

        # room model 의 숙박 한도 인원 검사
        if value.get('guest_personnel') and room.rooms_personnel < value['guest_personnel']:
            raise serializers.ValidationError('숙박 허용 인원을 초과했습니다.')

        # 기존 예약 목록 수집
        reservation_list = []
        reservation_instance = room.room_reservations.all()

        for date in reservation_instance:
            start_date = date.checkout - date.checkin
            reservation_list += [date.checkin + timedelta(n) for n in range(start_date.days + 1)]

        checkin = value.get('checkin')
        checkout = value.get('checkout')

        # 체크 인, 체크 아웃 필드 채워졌는지 검사
        if not checkin:
            raise serializers.ValidationError(detail='check-in 정보가 입력되지 않았습니다.',
                                              status=status.HTTP_400_BAD_REQUEST)

        elif not checkout:
            raise serializers.ValidationError(detail='check-out 정보가 입력되지 않았습니다.',
                                              status=status.HTTP_400_BAD_REQUEST)

        # 잘못된 예약 예외처리, 체크 인 이 체크 아웃보다 뒷 일자 일 수 없고, 체크 인 과 체크 아웃 이 같은 일자 일 수가 없다.

        if checkin > checkout or checkin == checkout:
            raise serializers.ValidationError(detail='잘못된 예약입니다.', status=status.HTTP_400_BAD_REQUEST)

        # 체크 인, 체크 아웃 필드 중복 검사, 이전 다른 사람이 먼저 예약 하였다면 예약 실패 처리
        for day in reservation_list:
            if day < checkin or day > checkout:
                pass
            else:
                raise serializers.ValidationError('예약할 수 없는 일자입니다.')

        return value

    def create(self, validated_data):
        # reservation = super().create(validated_data)
        # return reservation
        return RoomReservation.objects.create(**validated_data)


class RoomFacilitieSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomFacilities
        fields = (
            'facilities',
        )


class RoomRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomRules
        fields = (
            'rule_list',
        )


class RoomDetailSerializer(serializers.ModelSerializer):
    rooms_host = UserSerializer()
    room_facilities = RoomFacilitieSerializer(many=True)
    room_reservations = RoomReservationSerializer(many=True)
    room_rules = RoomRuleSerializer(many=True)
    room_images = RoomImageSerializer(many=True)
    rooms_cover_image = serializers.ImageField()

    class Meta:
        model = Rooms
        fields = (
            'pk',
            'rooms_type',
            'rooms_name',
            'rooms_tag',
            'rooms_host',
            'rooms_cover_image',
            'rooms_type',
            'room_images',
            'rooms_amount',
            'rooms_bed',
            'rooms_personnel',
            'rooms_bathroom',
            'days_price',
            'room_rules',
            'room_facilities',
            'rooms_description',
            'check_in_minimum',
            'check_in_maximum',
            'room_reservations',
            'refund',
            'address_country',
            'address_city',
            'address_district',
            'address_detail',
            'address_latitude',
            'address_longitude',
            'created_at',
            'modified_date',
        )
