from django.contrib import admin

# Register your models here.
from .models import Rooms, RoomDetail, RoomImage

admin.site.register(Rooms)
admin.site.register(RoomDetail)
admin.site.register(RoomImage)