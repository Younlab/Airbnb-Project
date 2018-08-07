from django.urls import path

from .views import room_list

app_name = 'rooms'

urlpatterns = [
    path('list/', room_list.RoomsList.as_view(), name='room_list'),
    path('list/<int:pk>/', room_list.RoomsDetail.as_view(), name='room_detail'),
    path('reservation/', room_list.RoomReservation.as_view()),
]
