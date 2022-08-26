from django.urls import path
from . import views
urlpatterns = [
    path('', view=views.index, name='index'),
    path('products/', view=views.Products, name='products'),
    path('product/<int:id>/', view=views.product_detail, name='product'),
]
