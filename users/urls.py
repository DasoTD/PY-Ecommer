from django.urls import path
from . import views
from django.contrib.auth import views as authentication_view

app_name = 'users'
urlpatterns = [
    path('register/', view=views.register, name='register'),
    path('login/', authentication_view.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', authentication_view.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', view=views.profile, name='profile'),
    path('createprofile/', view=views.create_profile, name='createprofile'),
    path('sellerprofile/<int:id>', view=views.seller_profile, name='sellerprofile')

] 
