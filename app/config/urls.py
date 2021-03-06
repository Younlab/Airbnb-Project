from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')),
    path('rooms/', include('rooms.urls')),
] + static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)


