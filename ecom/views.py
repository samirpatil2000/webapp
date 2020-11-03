from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView,DetailView

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from .models import ProductInCart,Product,Order,Category,Address
from .forms import AddressForm


class HomeView(ListView):
    model = Product
    template_name = 'ecom/index.html'
    context_object_name = 'object'
    # def get(self,*args,**kwargs):

class ProductListView(ListView):
    model = Product
    template_name = 'ecom/shop-grid.html'
    context_object_name = 'object'

def productList(request):

    template_name = 'ecom/shop-grid.html'
    cat=Category.objects.all()
    list=Product.objects.all()

    context={
        'categories':cat,
        'object':list
    }
    return render(request,template_name,context)

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



def add_single_item_to_cart(request, slug):
    product=get_object_or_404(Product,slug=slug)
    order_product,created=ProductInCart.objects.get_or_create(user=request.user,product=product)

    orders=Order.objects.filter(user=request.user)
    if orders.exists():
        order=orders[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity+=1
            order_product.save()
            messages.success(request,f"Updated {product.name} with {order_product.quantity}")
            return redirect("cart")
        else:
            order_product.quantity=1
            order_product.save()
            # order.products.add(order_product)
            messages.success(request, f"Added {product.name} ")
            return redirect("cart")
    else:
        order=Order.objects.create(user=request.user)
        order.products.add(order_product)
        messages.success(request,f'{product.name} is added to your cart')
        return redirect("cart")


def remove_single_item_from_cart(request, slug):
    product=get_object_or_404(Product,slug=slug)
    order_product,created=ProductInCart.objects.get_or_create(user=request.user,product=product)

    orders=Order.objects.filter(user=request.user)
    if orders.exists():
        order=orders[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity-=1
            order_product.save()
            messages.success(request,f"Updated {product.name} with {order_product.quantity}")
            return redirect("cart")
    else:
        order=Order.objects.create(user=request.user)
        order.products.add(order_product)
        messages.success(request,f'{product.name} is added to your cart')
        return redirect("cart")


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
            order_product.delete()
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



#TODO THIS IS THE HOME PAGE
def search(request):
    search_result=''
    qs = Product.objects.all()
    cat=Category.objects.all()

    title_contains_query = request.GET.get('search_all')
    if title_contains_query !='' and title_contains_query is not None:
        qs=qs.filter(name__icontains=title_contains_query)

    context={
        'object':qs,
        'categories':cat
        }
    return render(request,'ecom/index.html',context)
def category_detail(request,slug):
    cat=get_object_or_404(Category,slug=slug)
    qs=Product.objects.filter(category=cat)
    cats=Category.objects.all()


    context={
        'object': qs,
        'cat':cat,
        'categories': cats,

    }
    return render(request,'ecom/shop-grid-cat-filter.html',context)

@login_required
def checkoutPage(request):
    save_address=Address.objects.filter(user=request.user,is_save=True)
    context={

    }
    address_form=AddressForm(request.POST or None)

    if request.method == 'POST':

        """
        user=request.user
        name=request.POST['name']
        address_1=request.POST['address_1']
        address_2=request.POST['address_2']
        mobile_number=request.POST['mobile_number']
        zipcode=request.POST['zipcode']
        city=request.POST['city']
        is_save=request.POST['is_save']
        address=Address.objects.create(
            user=user,
            name=name,
            address_1=address_1,
            address_2=address_2,
            mobile_number=mobile_number,
            zipcode=zipcode,
            city=city,
            is_save=is_save,
        )
        address.save()
        
        """

        if address_form.is_valid():
            add_address=address_form.save(commit=False)
            address_form.instance.user=request.user
            add_address.save()
            messages.info(request,'Moving to payment')
            return redirect('checkout')

    return render(request,'ecom/checkout.html',{'form':address_form,'address':save_address})

def update_detail_address(request,id):
    pass