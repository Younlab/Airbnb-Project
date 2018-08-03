from django.conf import settings
from django.db import models

__all__ = (
    'Rooms',
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

    # rooms_detail = models.ManyToManyField(
    #     RoomDetail,
    #     related_name='room_details',
    # )

    tag = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.rooms_name
