from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Vet(models.Model):
    username = models.CharField(max_length=250, null=False)
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    contact = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    fees = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.username


class Appointment(models.Model):
    appointment_status = models.BooleanField(default=True)
    payment_status = models.BooleanField(default=True)
    user_username = models.ForeignKey(User, on_delete=models.CASCADE)
    vet_username = models.ForeignKey(Vet, on_delete=models.CASCADE)
    appointment_created_date = models.DateTimeField()
    appointment_date = models.DateTimeField()
    cancel = models.BooleanField(default=False)
    cancel_reason = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.user_username.username
