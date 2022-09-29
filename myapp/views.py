from distutils.command.build import build
from distutils.command.upload import upload
from statistics import mode
from unicodedata import name
from django.shortcuts import render, redirect
from .models import Product, OrderDetail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
# Create your views here.

def index(request):
    return HttpResponse("course")

def Products(request):
    page_obj = products = Product.objects.all()

    product_name = request.GET.get('product_name')
    if product_name != '' and product_name is not None:
        page_obj = products.filter(name__icontains=product_name)
    paginator = Paginator(page_obj,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # context = {
    #     'products': products
    # }
    context = {
        'page_obj' : page_obj
    }
    return render(request, 'index.html', context)

# class based list view
class ProductListView(ListView):
    model= Product
    template_name= 'index.html'
    context_object_name= 'products'
    paginate_by= 3

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
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs) :
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        # return super().get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

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
# class based createView
class ProductCreateView(CreateView):
    model= Product
    fields= ['name', 'price', 'description', 'image', 'seller_name']

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

class ProductUpdateView(UpdateView):
    model= Product
    fields= ['name', 'price', 'description', 'image', 'seller_name']
    template_name_suffix=  '_update_form'

def delete_product(request, id):
    product = Product.objects.get(id=id);
    context = {
        'product': product
    }
    if request.method == 'POST':
        product.delete()
        return redirect('/products')
    return render(request, 'delete.html', context)
class ProductDelete(DeleteView):
    model= Product
    success_url= reverse_lazy('myapp:products')


def my_listing(request):
    products = Product.objects.filter(seller_name=request.user)
    context = {
        'products' : products
    }
    return render(request, 'mylisting.html', context)

@csrf_exempt
def create_checkout_sesseion(request, id):
    product = get_object_or_404(Product, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email = request.user.email,
        payment_method_types = ['card'],
        line_items = [
            {
            "price_data"  : {
                'currency': 'usd',
                'product_data': {
                    'name': product.name,

                },
                'unit_amount': int(product.price *100),
            },
            'quantity': 1,
        }
        ],
        mode= 'payment',
        success_url = request.build_absolute_uri(reverse('mayapp:success'))+"?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('mayapp:failed')),
    )

    order = OrderDetail()
    order.customer_username= request.user.username
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price*100)
    order.save()
    return JsonResponse({'sessionId': checkout_session.id })


class PaymentSuccessView(TemplateView):
    template_name = 'myapp/payment_success.html'

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        stripe.checkout.Session.retrieve(session_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)

class PaymentFailedView(TemplateView):
    template_name = 'myapp/payment_failed.html'