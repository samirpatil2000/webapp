from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView,DetailView

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from .models import ProductInCart,Product,Order


class HomeView(ListView):
    model = Product
    template_name = 'ecom/index.html'
    context_object_name = 'object'


class ProductList(ListView):
    model = Product
    template_name = 'ecom/shop-grid.html'
    context_object_name = 'object'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'ecom/shop-details.html'
    context_object_name = 'object'

def ProductDeatilFBView(request,slug):
    detailData=Product.objects.get(slug=slug)

    # TODO related meance use filter with category field

    # related_product=
    template_name = 'ecom/shop-details.html'
    context={
        'object':detailData
    }
    return render(request,template_name,context)

@login_required
def add_to_cart(request,slug):
    product=get_object_or_404(Product,slug=slug)
    order_product,created=ProductInCart.objects.get_or_create(user=request.user,product=product)

    orders=Order.objects.filter(user=request.user)
    if orders.exists():
        order=orders[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity+=1
            order_product.save()
            messages.success(request,f"Updated {product.name} with {order_product.quantity}")
            return redirect("shop-detail",slug=slug)
        else:
            order.products.add(order_product)
            messages.success(request, f"Added {product.name} ")
            return redirect("shop-detail",slug=slug)
    else:
        order=Order.objects.create(user=request.user)
        order.products.add(order_product)
        messages.success(request,f'{product.name} is added to your cart')
        return redirect("shop-detail",slug=slug)


def add_to_cart_with_number(request,slug):
    val=request.POST.get('quantity')
    value=int(val)
    if value==0:
        raise
    else:
        product=get_object_or_404(Product,slug=slug)
        order_product,created=ProductInCart.objects.get_or_create(user=request.user,product=product)

        orders=Order.objects.filter(user=request.user)
        if orders.exists():
            order=orders[0]
            if order.products.filter(product__slug=product.slug).exists():
                order_product.quantity+=value
                order_product.save()
                messages.success(request,f"Updated {product.name} with {order_product.quantity}")
                return redirect("shop-detail",slug=slug)
            else:
                order_product.quantity=value
                order_product.save()
                # order.products.add(order_product)
                messages.success(request, f"Added {product.name} ")
                return redirect("shop-detail",slug=slug)
        else:
            order=Order.objects.create(user=request.user)
            order.products.add(order_product)
            messages.success(request,f'{product.name} is added to your cart')
            return redirect("shop-detail",slug=slug)

def remove_from_cart(request,slug):
    product=get_object_or_404(Product,slug=slug)

    orders=Order.objects.filter(user=request.user,is_ordered=False)
    if orders.exists():
        order=orders[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product= ProductInCart.objects.filter( product=product,
                                                         user=request.user,
                                                         )[0]
            order.products.remove(order_product)
            messages.success(request,f" {product.name}  removed ")
            return redirect("shop-detail",slug=slug)
        else:
            messages.success(request,  "This product is not in your cart")
            return redirect("shop-detail",slug=slug)
    else:
        messages.success(request,f' You donot have such product in your cart ')
        return redirect("shop-detail",slug=slug)




def shoppingCart(request):
    try:
        products=Order.objects.get(user=request.user,is_ordered=False)
        context={
            'object':products,
        }
        return render(request,'ecom/shoping-cart.html',context)
    except ObjectDoesNotExist :
        messages.warning(request, "You do not have an active order")
        redirect('index')

class ShoppingCart(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order=Order.objects.get(user=self.request.user,is_ordered=False)
            context={
                'object':order
            }
            return render(self.request,'account/index.html',context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect('index')

@login_required
def add_to_fav(request,slug):
    prod=get_object_or_404(Product,slug=slug)
    qs=Product.objects.filter(favourite=request.user)
    if qs.exists():
        messages.warning(request," You already added ")
    else:
        messages.info(request, f" {prod.name} is added")
        prod.favourite.add(request.user)

    return redirect("shop-detail", slug=slug)

@login_required
def remove_from_fav(request,slug):
    prod=get_object_or_404(Product,slug=slug)
    qs=Product.objects.filter(favourite=request.user)
    if qs.exists():
        prod.favourite.remove(request.user)
        messages.warning(request,f"{prod.name} is removed from favourite")
    else:
        messages.warning(request," You don't have this product in your fav")

    return redirect("shop-detail", slug=slug)

@login_required
def favList(request):
    try:
        obj=Product.objects.filter(favourite=request.user)
        context={
            'object':obj
        }
        return render(request,'account/index.html',context)

    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        redirect('index')




