from rest_framework import serializers

from ..models import Rooms


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = (
            'host',
            'rooms_name',
            'tag'
        )


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'
