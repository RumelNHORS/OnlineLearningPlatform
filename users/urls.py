from django.urls import path
from users.views import profile, request_account

app_name = 'users'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('request/', request_account, name='request_account')
]
