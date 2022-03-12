from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminlogin, name='adminlogin'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('adminlogout/', views.logoutadmin, name ='adminlogout'),
    path('index/', views.dashboard, name='adminindex'),
    path('adminregister/', views.register, name='admin-register'),


]
