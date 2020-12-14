from django.contrib import admin
from .models import ProductInCart,Product,Order,Category,Address,Transaction,IP,Image
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductInCart)
admin.site.register(Order)

admin.site.register(Category)

admin.site.register(Address)

admin.site.register(Transaction)

#Changing for add to cart
admin.site.register(IP)

admin.site.register(Image)



#TODO Tasks
#Checkout
#Favourites
