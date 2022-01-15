from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminlogin, name='admin_login'),


]
