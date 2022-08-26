from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("course")

def Products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'index.html', context)

def product_detail(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'detail.html',  context) 
