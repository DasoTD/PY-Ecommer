from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', view=views.register, name='register'),
    
] 
