from django.urls import path

from . import views

app_name = 'images'

urlpatterns = [
    path('', views.ImageListCreateView.as_view(), name='list_create'),
    path('<int:pk>/', views.ImageRetriveAPIView.as_view(), name='img_details'),
    path('create_temp_url/<int:pk>/<int:seconds>/',
         views.TempURLCreateView.as_view(), name='create_temp'),
    path('temp/<str:pk>/', views.TempURLView.as_view(), name='temp_url'),
]
