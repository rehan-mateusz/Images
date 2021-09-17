from django.urls import path

from . import views

app_name = 'images'

urlpatterns = [
    path('', views.ImageListCreateView.as_view()),
    path('<int:pk>/', views.ImageRetriveAPIView.as_view()),
    path('create_temp_url/<int:pk>/<int:seconds>/', views.TempURLCreateView.as_view()),
    path('temp/<str:pk>/', views.TempURLView.as_view(), name='temp_url'),
]
