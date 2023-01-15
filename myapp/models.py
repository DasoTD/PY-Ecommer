from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
# Create your models here.

class Product(models.Model):
    seller_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    image= models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('myapp:products')

class OrderDetail(models.Model):
    customer_username = models.CharField(max_length=200)
    product = models.ForeignKey(to='Product', on_delete=models.PROTECT)
    amount = models.IntegerField()
    stripe_payment_intent = models.CharField(max_length=200)
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
class OrderHistory(models.Model):
    orderID = models.ForeignKey(to="OrderDetail", on_delete=models.CASCADE)
# from django.contrib.auth.models import User
# # Create your models here.
# class Profile(models.Model):
#     def __str__(self):
#         return self.user.username
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(default='profile.jpg', upload_to='profile_pictures')
#     contact_number = models.CharField(max_length=100, default='999999999')
