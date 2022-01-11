from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('loginn/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('product', views.products, name="products"),
    path('appointent', views.appointment, name="appointment"),
    path('', views.home, name='Home'),

]
