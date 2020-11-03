from django.contrib import admin
from .models import ProductInCart,Product,Order,Category,Address
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductInCart)
admin.site.register(Order)

admin.site.register(Category)

admin.site.register(Address)



#TODO Tasks
#Checkout
#Favourites
