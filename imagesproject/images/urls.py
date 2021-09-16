from django.urls import path

from . import views

app_name = 'images'

urlpatterns = [
    path('', views.ImageListCreateView.as_view()),
    path('<int:pk>/', views.ImageRetriveAPIVIew.as_view()),
]
