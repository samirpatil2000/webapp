from django.shortcuts import render

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