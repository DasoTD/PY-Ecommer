from unicodedata import name
from django.shortcuts import render, redirect
from .models import Product
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
# Create your views here.

def index(request):
    return HttpResponse("course")

def Products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'index.html', context)

# class based list view
class ProductListView(ListView):
    model= Product
    template_name= 'index.html'
    context_object_name= 'products'

def product_detail(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'detail.html',  context) 

    # class based detail view
class ProductDetailView(DetailView):
    model= Product
    template_name= 'detail.html'
    context_object_name= 'product'


@login_required
def add_product(request):
    if request.method == 'POST' :
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES['upload']
        seller_name = request.user
        product = Product(name=name, price=price, description=description, image=image, seller_name=seller_name)
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
def my_listing(request):
    products = Product.objects.filter(seller_name=request.user)
    context = {
        'products' : products
    }
    return render(request, 'mylisting.html', context)
