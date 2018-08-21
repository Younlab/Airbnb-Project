import datetime
from datetime import timedelta

import arrow

from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404

from members.serializers.user import UserSerializer
from rooms.models.reservation import ReservationReserved
from ..models import RoomFacilities, RoomRules, RoomImage, RoomReservation
from ..models import Rooms


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


class RoomImageSerializer(serializers.ModelSerializer):
    room_image = serializers.ImageField()

    class Meta:
        model = RoomImage
        fields = (
            'room_image',
        )


class RoomCreateSerializer(serializers.ModelSerializer):
    room_images = RoomImageSerializer(many=True, read_only=True)
    room_rules = RoomRuleSerializer(many=True, read_only=True)
    room_facilities = RoomFacilitieSerializer(many=True, read_only=True)
    rooms_host = UserSerializer(read_only=True)

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

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['rooms_host'] = request.user
        rooms = super().create(validated_data)

        # image cover
        for cover in request.data.getlist('rooms_cover_image'):
            rooms.rooms_cover_image.save(cover.name, cover)
        num = 1

        # image list
        if request.FILES:
            for covers in request.data.getlist('room_images'):
                # print(covers)
                rooms_images = RoomImage.objects.create(room=rooms)
                # print(rooms_images)
                rooms_images.room_image.save(f'image_list_no_{num}_{covers.name}', covers)
                num += 1

        for rule in request.data.getlist('rule_list'):
            rooms.room_rules.create(rule_list=rule)

        for facilities in request.data.getlist('facilities'):
            rooms.room_facilities.create(facilities=facilities)

        request.user.is_host = True
        request.user.save()
        return rooms


class ReservationReservedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationReserved
        fields = (
            'disable_days',
        )


class RoomListSerializer(serializers.ModelSerializer):
    rooms_cover_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = Rooms
        fields = (
            'pk',
            'rooms_type',
            'rooms_name',
            'rooms_tag',
            'days_price',
            'rooms_cover_thumbnail',
            'created_at',
        )


class RoomReservationSerializer(serializers.ModelSerializer):
    """
    숙소 예약
    """
    room = Rooms
    guest = UserSerializer(read_only=True)
    reservations_disable = ReservationReservedSerializer(read_only=True, many=True)

    class Meta:
        model = RoomReservation
        fields = (
            'room',
            'guest_personnel',
            'guest',
            'checkin',
            'checkout',
            'reservations_disable',
            'created_at',

        )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['guest'] = request.user
        reserved_save = super().create(validated_data)

        check_in = arrow.get(validated_data['checkin'])
        check_out = arrow.get(validated_data['checkout'])
        rooms = validated_data['room']
        # disable_days_list = rooms.room_reservations.all()
        # disable_days_instance = []
        #
        # for i in disable_days_list:
        #     staying_days = i.checkout - i.checkin
        #     disable_days_instance += [i.checkin + timedelta(n) for n in range(staying_days.days + 1)]
        #
        # print(disable_days_instance)
        # for day in disable_days_instance:
        #     if day < timedelta(check_in) or day > timedelta(check_out):
        #         pass
        #     else:
        #         raise Exception(detail='예약할 수 없는 날짜를 선택하셨습니다.', status_code=status.HTTP_400_BAD_REQUEST)
        # # print(disable_days_list)
        # for day in disable_days_instance:
        #     print(day)
        #     if day < check_ins or day > check_outs:
        #         pass
        #     else:
        #         raise Exception(detail='예약할 수 없는 날짜를 선택하셨습니다.', status_code=status.HTTP_400_BAD_REQUEST)

        reserved_range = check_out - check_in
        reserved_list = []
        for i in range(reserved_range.days + 1):
            reserved_list.append(check_in + timedelta(i))

        for l in reserved_list:
            ReservationReserved.objects.create(room=RoomReservation.objects.filter(room=rooms).first(),
                                               disable_days=l.date())

        return reserved_save


class RoomDetailSerializer(serializers.ModelSerializer):
    rooms_host = UserSerializer(read_only=True)
    room_facilities = RoomFacilitieSerializer(many=True)
    room_reservations = RoomReservationSerializer(many=True)
    room_rules = RoomRuleSerializer(many=True)
    room_images = RoomImageSerializer(many=True)
    rooms_cover_image = serializers.ImageField()

    class Meta:
        model = Rooms
        fields = (
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
