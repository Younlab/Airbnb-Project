from django.urls import path

from .views import room_list, room_like

app_name = 'rooms'

urlpatterns = [
    # 메인 room list
    path('main/', room_list.MainPageRoomsList.as_view(), name='main_list'),
    path('main/<int:room_pk>/', room_list.RoomsDetail.as_view(), name='main_detail'),
    path('main/<int:room_pk>/reservation/', room_list.RoomReservationAPI.as_view(), name='main_reservation'),

    # 기본 room list
    path('list/', room_list.RoomsList.as_view(), name='room_list'),
    path('list/<int:room_pk>/', room_list.RoomsDetail.as_view(), name='room_detail'),
    path('list/<int:room_pk>/reservation/', room_list.RoomReservationAPI.as_view(), name='room_reservation'),
    path('list/<int:pk>/likes/', room_like.RoomsLikes.as_view(), name='room_like'),
]
