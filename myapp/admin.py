from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Product)
admin.site.site_header=("Buy and Sell Website")
admin.site.site_title=("e-commerce") 
admin.site.index_title=("manage e-commerce site")