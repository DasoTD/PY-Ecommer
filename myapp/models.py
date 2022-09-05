from distutils.command.upload import upload
from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    image= models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.name
