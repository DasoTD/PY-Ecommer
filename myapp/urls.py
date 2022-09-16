from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', view=views.index, name='index'),
    path('products/', view=views.Products, name='products'),
    path('product/<int:id>/', view=views.product_detail, name='product'),
    path('product/add/', view=views.add_product, name='addproduct'),
    path('product/update/<int:id>', view=views.update_product, name='updateproduct'),
    path('product/delete/<int:id>', view=views.delete_product, name='deleteproduct'),
    path('product/mylisting/', view=views.my_listing, name='muylisting'),
] 
