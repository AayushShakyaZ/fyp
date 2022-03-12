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


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)


def __str__(self):
    return self.name


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(unique=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(upload_to="products")
    price = models.PositiveIntegerField(null=True, blank=False)

    def __str__(self):
        return self.title


METHOD = {
    ("Khalti", "Khalti"),
}


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    payment_method = models.CharField(max_length=20, default=False, choices=METHOD)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
