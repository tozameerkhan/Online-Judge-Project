"""
URL configuration for Online_Judge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('welcomeapp.urls', namespace='welcomeapp')),
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls', namespace='accounts')),
    path('home/', include('home.urls', namespace='home')),
    path('profile/', include('userprofile.urls', namespace='userprofile')),
    path('problem/', include('problems.urls', namespace='problems')),
]
