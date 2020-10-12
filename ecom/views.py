from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView,DetailView
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



