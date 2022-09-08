from unicodedata import name
from django.shortcuts import render, redirect
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

def add_product(request):
    if request.method == 'POST' :
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES['upload']
        product = Product(name=name, price=price, description=description, image=image)
        product.save()
        return redirect('/')
    else:
        return render(request, 'addproduct.html')

def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        if request.FILES.get('image') == None:
            product.name = request.POST.get('name')
            product.price = request.POST.get('price')
            product.description = request.POST.get('description')
            product.save()

        if request.FILES.get('image') != None:
            product.name = request.POST.get('name')
            product.price = request.POST.get('price')
            product.description = request.POST.get('description')
            product.image = request.FILES['upload']
            product.save()
        return redirect('/products')
    context = {
        'product': product
    }
    return render(request, 'updateproduct.html', context)

def delete_product(request, id):
    product = Product.objects.get(id=id);
    context = {
        'product': product
    }
    if request.method == 'POST':
        product.delete()
        return redirect('/products')
    return render(request, 'delete.html', context)