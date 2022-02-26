import datetime
from math import ulp
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.views import View

from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.views.generic import TemplateView
import json


def registerPage(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.info(request, 'Username or Password is Incorrect')

    context = {}
    return render(request, 'loginn.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'index.html')


def appointment(request):
    vet = Vet.objects.all().filter(is_active=True)
    content = {
        "vet": vet
    }
    return render(request, 'appointment.html', content)


def appointment_form(request, username):
    vet = Vet.objects.all().filter(username=username)
    user = User.objects.all().filter(username=request.user.username)
    user_first = user.first()

    print(vet)
    if request.method == "POST":
        app_datetime = request.POST['datetime']

        appointment_status = True
        payment_status = False
        user_obj = user_first
        vet_obj = vet.first()
        appointment_created_date = datetime.datetime.now()
        appointment_date = app_datetime
        cancel = False
        new_appointment = Appointment.objects.create(appointment_status=appointment_status,
                                                     payment_status=payment_status, user_username=user_obj,
                                                     vet_username=vet_obj,
                                                     appointment_created_date=appointment_created_date,
                                                     appointment_date=appointment_date, cancel=cancel)
        new_appointment.save()
        contnt_succes = {
            'vet_obj': vet_obj
        }
        return render(request, "success.html", contnt_succes)

    content = {
        'vet': vet,
        'user': user
    }
    return render(request, 'appointment_form.html', content)


def appointment_history(request):
    username = request.user.username
    appointment = Appointment.objects.all().filter(user_username=request.user)
    content = {'appointment': appointment}
    return render(request, 'appointment_history.html', content)


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    prods = Product.objects.all()
    context = {'prods': prods, 'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item Added to cart', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrderItem.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
            )
    else:
        print('user is not logged in!')
    return JsonResponse('Payment Successful', safe=False)


class CategoryView(TemplateView):
    template_name = "category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class EsewaRequestView(View):
    def get(self, request, *args, **kwargs):
        content = {

        }
        return render(request, "esewarequest.html", content)
