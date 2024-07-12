from django.urls import path, include
from home.views import homepage


urlpatterns = [
    path("homepage/", homepage,name = "home-page"),
    #path("profile/", homepage,name = "profile"),
]