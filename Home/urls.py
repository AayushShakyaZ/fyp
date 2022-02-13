from django.urls import path
from . import views
from .views import CategoryView

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('loginn/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('appointment', views.appointment, name="appointment"),
    path('appointment_form/<str:username>', views.appointment_form, name="appointment_form"),
    path('appointment_form', views.appointment_form, name="appointment_form"),
    path('appointment_history', views.appointment_history, name="view_appointment_history"),
    path('', views.home, name='Home'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path("category/", CategoryView.as_view(), name="category")

]
