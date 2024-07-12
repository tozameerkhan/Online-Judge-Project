from django.urls import path, include
from userprofile.views import update_profile

app_name = 'userprofile'  

urlpatterns = [
    #path("profile/", profiles,name = "user_profile"),
    path("profile/", update_profile, name='update_profile'),
]