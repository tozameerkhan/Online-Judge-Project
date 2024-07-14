from django.urls import path
from userprofile.views import update_profile

app_name = 'userprofile'

urlpatterns = [
    path('update/', update_profile, name='update_profile'),
]
