from django.urls import path
from userprofile.views import update_profile,view_profile, update_password

app_name = 'userprofile'

urlpatterns = [
    path('view/', view_profile, name='view_profile'),
    path('update/', update_profile, name='update_profile'),
    path('update_password/', update_password, name='update_password'),
]
