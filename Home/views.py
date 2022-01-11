from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
    return render(request, 'product.html')


def appointment(request):
    return render(request, 'appointment.html')
