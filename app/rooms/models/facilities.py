from django.db import models
from .rooms import Rooms

__all__ = (
    'RoomFacilities',
)


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
