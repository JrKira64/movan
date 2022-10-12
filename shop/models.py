from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    prouser = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.prouser.username

class Roadtrip(models.Model):
    From = models.CharField(max_length=200)
    to = models.CharField(max_length=200)
    Date= models.DateField(blank=True, null=True)
    def __str__(self):
        return f"From=={self.From}<==>To:{self.to}==Date=={self.Date}"



class Cart(models.Model):
    customer = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)
    complit = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

class CartBooking(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    roadtrip = models.ManyToManyField(Roadtrip)
   
    def __str__(self):
        return f"Cart=={self.cart.id}<==>CartBooking:{self.id}"


class Order(models.Model):
    cart  = models.OneToOneField(Cart,on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=16)
    email = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    payment_complit = models.BooleanField(default=False,blank=True, null=True)



