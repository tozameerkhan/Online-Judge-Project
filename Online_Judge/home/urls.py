from django.urls import path, include
from home.views import homepage

app_name = 'home'
urlpatterns = [
    path("homepage/", homepage,name = "home-page"),
]