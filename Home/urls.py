from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('loginn/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('product', views.products, name="products"),
    path('appointment', views.appointment, name="appointment"),
    path('appointment_form/<str:username>', views.appointment_form, name="appointment_form"),
    path('appointment_form', views.appointment_form, name="appointment_form"),
    path('appointment_history', views.appointment_history, name="view_appointment_history"),
    path('', views.home, name='Home'),


]
