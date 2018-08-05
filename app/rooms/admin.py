from django.contrib import admin

# Register your models here.
from .models import Rooms, RoomFacilities, RoomImageList

admin.site.register(Rooms)
admin.site.register(RoomFacilities)
admin.site.register(RoomImageList)
