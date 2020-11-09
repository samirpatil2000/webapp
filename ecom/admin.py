from django.contrib import admin
from .models import ProductInCart,Product,Order,Category,Address,Transaction,IP
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductInCart)
admin.site.register(Order)

admin.site.register(Category)

admin.site.register(Address)

admin.site.register(Transaction)

#Changing for add to cart
admin.site.register(IP)



#TODO Tasks
#Checkout
#Favourites
