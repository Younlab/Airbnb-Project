from django.urls import path

from . import views

app_name = 'rooms'

urlpatterns = [
    # 메인 room list
    path('main/', views.MainPageRoomsList.as_view(), name='main_list'),
    path('main/<int:room_pk>/', views.RoomsDetail.as_view(), name='main_detail'),
    path('main/<int:room_pk>/reservation/', views.RoomReservationAPI.as_view(), name='main_reservation'),

    # 기본 room list
    path('list/', views.RoomsList.as_view(), name='room_list'),
    path('list/<int:room_pk>/', views.RoomsDetail.as_view(), name='room_detail'),
    path('list/<int:room_pk>/reservation/', views.RoomReservationAPI.as_view(), name='room_reservation'),
    path('list/<int:pk>/likes/', views.RoomsLikes.as_view(), name='room_like'),

    # 숙소 등록 room create
    path('create/', views.RoomsCreate.as_view(), name='room_create'),
]
