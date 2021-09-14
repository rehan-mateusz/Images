from django.urls import path

from . import views

app_name = 'images'

urlpatterns = [
    path('images/', views.ImageListCreateView.as_view()),
]
