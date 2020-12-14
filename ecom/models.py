from django.db import models

# Create your models here.
from django.db import models
import random
from django.conf import settings
from django.utils import timezone

# Create your models here.
from django.urls import reverse

from django.core.validators import MinValueValidator,MaxValueValidator

CATEGORY_CHOICE=(
    ('B','Bread'),
    ('E','Egg'),
    ('M','Milk'),
    ('C','Chips'),
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
def default_cat():
    cat_list=['Bread','Milk','Eggs','Chips','Butter & Cheese']
    n=random.randrange(0,len(cat_list))
    return cat_list[n]




class Image(models.Model):
    Product=models.ForeignKey('Product',on_delete=models.CASCADE,related_name='product_images',blank=True,null=True)
    image=models.ImageField(upload_to='product_images')


    def __str__(self):
        return self.Product.name


class Category(models.Model):
    name=models.CharField(default=default_cat,max_length=100)
    slug=models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to='cat_images', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_cat_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})


class Product(models.Model):
    name=models.CharField(max_length=100,default=default_product_name)
    desc=models.TextField(default="This is the desc of product")
    price=models.IntegerField(default=default_product_price)
    #category=models.CharField(choices=CATEGORY_CHOICE,max_length=1)
    category=models.ManyToManyField(Category)
    slug=models.SlugField()
    list_product=models.BooleanField(default=True)
    favourite=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,null=True)

    thumbnail=models.ImageField(upload_to='product_images',blank=True,null=True)

    images=models.ManyToManyField(Image,blank=True)


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

    def get_remove_single_from_cart_url(self):
        return reverse('remove_single_from_cart',kwargs={'slug':self.slug})

    def get_add_single_to_cart_url(self):
        return reverse('add_single_to_cart',kwargs={'slug':self.slug})


class IP(models.Model):
    pub_date = models.DateTimeField('date published',default=timezone.now())
    ip_address = models.GenericIPAddressField()



class ProductInCart(models.Model):
    #user_ip=models.ForeignKey(IP,on_delete=models.CASCADE,default='127.0.0.1')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    #order_date=models.DateTimeField(default=timezone.now())
    quantity=models.IntegerField(default=1)

    def __str__(self):
        # return f'{self.user_ip} , {self.product} , {self.quantity}'
        return f'{self.user.email} , {self.product} , {self.quantity}'

    def get_total_price(self):
        return self.product.price * self.quantity

    def get_total_discount_price(self):
        return self.product.price * self.quantity


    def get_final_amount(self):
        if self.product.price:
            return self.get_total_price()
        return self.get_total_discount_price()



class Address(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(default='Hostel',max_length=20)
    address_1=models.CharField(default='Address',max_length=200)
    address_2=models.CharField(default='Address',max_length=200,blank=True,null=True)
    mobile_number=models.IntegerField(default='1234567890',blank=True,null=True,
                                      validators=[
                                          MinValueValidator(999999999),
                                          MaxValueValidator(9999999999)
                                      ])
    zipcode=models.IntegerField(default='400035',
                                validators=[
                                    MinValueValidator(99999),
                                    MaxValueValidator(999999)
                                ])
    city=models.CharField(default='mumbai',max_length=20)
    is_save=models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.email} -- {self.name}'

    # def get_absolute_order_url(self):
    #     return reverse('order_history_detailview',kwargs={'id':self.pk})


class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_ordered=models.BooleanField(default=False)
    ordered_date=models.DateTimeField(default=timezone.now())
    products=models.ManyToManyField(ProductInCart)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.user.email

    def get_total_amount(self):
        total_amount=0
        for prod in self.products.all():
            total_amount+=prod.get_final_amount()
        return total_amount

    def get_total_quantity_per_order(self):
        total_quantity=0
        for i in self.products.all():
            total_quantity+=i.quantity
        return total_quantity



    # def get_absolute_order_url(self):
    #     return reverse('order_history_detailview',kwargs={'id':self.pk})


class Transaction(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    trans_date=models.DateTimeField(default=timezone.now())
    payment_method=models.CharField(default='COD',max_length=20)

    address_name = models.CharField(default='Hostel', max_length=20)
    address_address_1 = models.CharField(default='Address', max_length=200)
    address_address_2 = models.CharField(default='Address', max_length=200, blank=True, null=True)
    address_mobile_number_verified = models.IntegerField(default='1234567890',
                                        validators=[
                                            MinValueValidator(999999999),
                                            MaxValueValidator(9999999999)
                                        ])
    address_mobile_number_2 = models.IntegerField(default='1234567890',blank=True, null=True,
                                                validators=[
                                                    MinValueValidator(999999999),
                                                    MaxValueValidator(9999999999)
                                                ])
    address_zipcode = models.IntegerField(default='400035',
                                  validators=[
                                      MinValueValidator(99999),
                                      MaxValueValidator(999999)
                                  ])
    address_city = models.CharField(default='mumbai', max_length=20)


    def __str__(self):
        return str(self.order.user.email)


    def get_absolute_order_url(self):
        return reverse('order_history_detailview',kwargs={'id':self.pk})


