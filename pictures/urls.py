from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pictures'
urlpatterns = [
    path('', views.PicturesListView.as_view(), name='all'),
    path('<int:pk>/', views.PictureDetailView.as_view(), name='picture_detail'),
    path('img/<int:pk>/', views.stream_file, name='img'),
    path('create/', views.PictureCreateView.as_view(success_url=reverse_lazy('pictures:all')), name='picture_create'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
