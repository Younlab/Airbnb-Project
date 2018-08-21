from django.conf import settings
from django.db import models
from .rooms import Rooms

__all__ = (
    'RoomReservation',
)


class RoomReservation(models.Model):
    """
    예약 등록
    """
    room = models.ForeignKey(
        Rooms,
        related_name='room_reservations',
        on_delete=models.CASCADE,
    )

    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    guest_personnel = models.PositiveSmallIntegerField(
        verbose_name='숙박 인원'
    )

    checkin = models.DateField(
        blank=True,
        verbose_name='체크인 날짜',
    )

    checkout = models.DateField(
        blank=True,
        verbose_name='체크아웃 날짜',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.guest}, {self.checkin}, {self.checkout}'

    class Meta:
        ordering = ['-created_at']


class ReservationReserved(models.Model):
    room = models.ForeignKey(
        RoomReservation,
        on_delete=models.CASCADE,
        related_name='reservations_disable'
    )

    disable_days = models.DateField(
        blank=True,
        null=True,
    )
