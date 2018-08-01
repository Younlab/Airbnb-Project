from django.db import models

__all__ = (
    'Facilities',
)

class Facilities(models.Model):
    """
    편의시설 연결
    """
    facilities = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.facilities
