from django.db import models

from .rooms import Rooms

__all__ = (
    'RoomRules',
)


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
