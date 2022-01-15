from django.shortcuts import render


# Create your views here.
def adminlogin(request):
    return render(request, 'admin_templates/admin_login.html')
