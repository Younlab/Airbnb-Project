from django.contrib import admin

# Register your models here.
from .models import Rooms as Rooms_editor, RoomFacilities, RoomRules, RoomImageList

admin.site.register(Rooms_editor)
admin.site.register(RoomImageList)
admin.site.register(RoomFacilities)
admin.site.register(RoomRules)
