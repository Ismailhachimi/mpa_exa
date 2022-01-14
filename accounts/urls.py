from django.urls import path
from accounts.api.views import get_token, refresh_token

urlpatterns = [
    path('token', get_token, name='get-token'),
    path('token/refresh', refresh_token, name='refresh-token'),
]
