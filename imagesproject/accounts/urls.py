from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
]
