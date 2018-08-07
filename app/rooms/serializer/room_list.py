from rest_framework import serializers

from ..models import Rooms


class RoomListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rooms
        fields = (
            'rooms_host',
            'rooms_name',
            'rooms_tag'
        )


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'
