from django.urls import path
from .views import welcomeapp

app_name = 'welcomeapp'

urlpatterns = [
    path('', welcomeapp, name='welcomeapp'),
]
