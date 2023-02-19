from json import load
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
# Create your views here.
import logging
import ipaddress


logger = logging.getLogger(__name__)

def my_view(request):
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")


def register(request):
    if request.method =='POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/products')
    form = NewUserForm()
    context = {
        "form": form
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    logger.debug("This is a debug message")
    print(request.user.id)
    client_ip = request.META['REMOTE_ADDR']
    ip = ipaddress.ip_address(client_ip)
    print(ip)
    # logger.info("This is an info message")
    # logger.warning("This is a warning message")
    # logger.error("This is an error message")
    return render(request, 'users/profile.html')

@login_required
def create_profile(request):
    if request.method == "POST":
        contact_number = request.POST.get('contact_number')
        image = request.FILES.get('upload')
        user = request.user
        profile = Profile(user=user,contact_number=contact_number, image=image)
        profile.save()
    return render(request, 'users/createprofile.html')

@login_required
def seller_profile(request, id):
    seller = User.objects.get(id=id)
    context ={
        'seller': seller
    }
    return render(request, 'users/sellerprofile.html', context)
