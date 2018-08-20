from django.db import models
from .rooms import Rooms

__all__ = (
    'RoomImage',
)


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
        max_length=255,
    )

    def __str__(self):
        return self.room_image
