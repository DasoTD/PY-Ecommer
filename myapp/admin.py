from django.contrib import admin
from . import models
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields= ('name','price')

    def set_price_to_zero(self, request, queryset):
        queryset.update(price=0)
        
    actions = ("set_price_to_zero",)

    list_editable = ('description', 'price')

admin.site.register(models.Product, ProductAdmin)
admin.site.site_header=("Buy and Sell Website")
admin.site.site_title=("e-commerce") 
admin.site.index_title=("manage e-commerce site")