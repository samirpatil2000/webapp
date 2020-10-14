from django.db import models

# Create your models here.
from django.db import models
import random
from django.conf import settings
from django.utils import timezone

# Create your models here.
from django.urls import reverse

CATEGORY_CHOICE=(
    ('B','Bread'),
    ('E','Egg'),
    ('M','Milk'),
)

def default_product_name():
    no1=random.randrange(1,9)
    no2=random.randrange(1,9)
    if no1==no2:
        return default_product_name()
    return 'product{}{}'.format(str(no1),str(no2))

def default_product_price():
    p=random.randrange(50,70)
    return p

def default_cat_choice():
    n=random.randrange(0,2)
    cat=CATEGORY_CHOICE[n]
    return cat





class Product(models.Model):
    name=models.CharField(max_length=100,default=default_product_name)
    desc=models.TextField(default="This is the desc of product")
    price=models.IntegerField(default=default_product_price)
    category=models.CharField(choices=CATEGORY_CHOICE,max_length=1)
    slug=models.SlugField()
    list_product=models.BooleanField(default=True)
    favourite=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,null=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop-detail',kwargs={'slug':self.slug})
    def get_add_to_cart_url(self):
        return reverse('add_to_cart',kwargs={'slug':self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart',kwargs={'slug':self.slug})

    def get_add_to_fav_url(self):
        return reverse('add_to_fav',kwargs={'slug':self.slug})
    def get_remove_from_fav_url(self):
        return reverse('remove_from_fav',kwargs={'slug':self.slug})

class ProductInCart(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    #order_date=models.DateTimeField(default=timezone.now())
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f'{self.user.email} , {self.product} , {self.quantity}'

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_ordered=models.BooleanField(default=False)
    ordered_date=models.DateTimeField(default=timezone.now())
    products=models.ManyToManyField(ProductInCart)

    def __str__(self):
        return self.user.email



# class Address(models.Model):
#     user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)