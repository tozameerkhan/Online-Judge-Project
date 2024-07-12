from django.urls import path, include
from accounts.views import register_user,login_user, logout_user


urlpatterns = [
    path('register/', register_user,name = "register-users"),
    path('login/', login_user,name='login-user'),
    path('logout/', logout_user,name='logout-user'),
]