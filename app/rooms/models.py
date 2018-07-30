from django.db import models


class Room(models.Model):
    # 편의 시설
    Facilities = models.CharField(max_length=400)
    # 객실 정보
    room_info = models.TextField()
    # 이용 규칙
    rule = models.TextField()
    # 가격 정보
    price = models.IntegerField()
    # 주소
    location = models.CharField(max_length=200)
