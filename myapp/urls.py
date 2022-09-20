from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', view=views.index, name='index'),
    path('products/', view=views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', view=views.ProductDetailView.as_view(), name='product'),
    path('product/add/', view=views.ProductCreateView.as_view() ,name='addproduct'),
    # path('product/update/<int:id>', view=views.update_product, name='updateproduct'),
    path('product/update/<int:pk>', view=views.ProductUpdateView.as_view(), name='updateproduct'),
    # path('product/delete/<int:id>', view=views.delete_product, name='deleteproduct'),
    path('product/delete/<int:pk>', view=views.ProductDelete.as_view(), name='deleteproduct'),
    path('product/mylisting/', view=views.my_listing, name='mylisting'),
] 
