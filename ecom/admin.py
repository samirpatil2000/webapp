from django.contrib import admin
from .models import ProductInCart,Product,Order
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductInCart)
admin.site.register(Order)
