import datetime
from math import ulp

from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *


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


def products(request):
    return render(request, 'store.html')


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
    prods = Product.objects.all()
    context = {'prods': prods}
    return render(request, 'store.html', context)


def cart(request):
    context = {}
    return render(request, 'cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)
