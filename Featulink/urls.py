"""
URL configuration for Featulink project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from flutelink.views import *
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('form/',registro_colaboracion, name='registro_colaboracion'),
    path('coincidencias/', mostrar_coincidencias, name='mostrar_coincidencias'),
    path('verificar/', verificar_registro, name='verificar_registro'),
    path('perfil/', user_profile, name='user_profile'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),



]
