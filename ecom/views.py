from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView,DetailView

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from .models import (ProductInCart,
                     Product,
                     Order,
                     Category,
                     Address,
                     Transaction,
                    Image,
                     IP,)
from .forms import (AddressForm,
                    UpdateAddress,
                    ChechoutForm,
                    ChechoutFormPaymentOption)

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def mobile_view(request):
    return render(request,'ecom/mobile-view.html')

class HomeView(ListView):
    model = Product
    template_name = 'ecom/index.html'
    context_object_name = 'object'
    # def get(self,*args,**kwargs):





"""IP ADDRESS"""
# testing for ip address
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')
        messages.info(request,"Meta Remote")
    get_ip = IP.objects.create(ip_address=ipaddress)  # imported class from model
    get_ip.save()
    messages.info(request,f"Your Ip Address Is {ipaddress}")
    return redirect('index')




#TODO THIS IS THE HOME PAGE
def search(request):
    search_result=''
    qs = Product.objects.all()
    cat = Category.objects.all()
    """
    bread =qs.filter(category__name='Bread')
    Milk =qs.filter(category__name='Milk')
    Eggs =qs.filter(category__name='Egg')
    Chips =qs.filter(category__name='Chips')
    butter =qs.filter(category__name='Butter and Cheese')
    """


    title_contains_query = request.GET.get('search_all')
    if title_contains_query !='' and title_contains_query is not None:
        qs=qs.filter(name__icontains=title_contains_query)

    # Create a paginator to split your products queryset
    paginator = Paginator(qs, 8)  # Show 1 contacts per page
    # Get the current page number
    page = request.GET.get('page')

    try:
        paginated_queryset=paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset=paginator.page(1)
    except EmptyPage: # showing last page
        paginated_queryset=paginator.page(paginator.num_pages)

    context={
        # 'object':qs,
        'object':paginated_queryset,
        'categories':cat,
        # 'breads':bread,
        # 'milk':Milk,
        # 'eggs':Eggs,
        # 'chips':Chips,
        # 'butter':butter,
        }
    return render(request,'ecom/index.html',context)




class ProductListView(ListView):
    model = Product
    template_name = 'ecom/shop-grid.html'
    context_object_name = 'object'


# This is the shop
def productList(request):

    template_name = 'ecom/shop-grid.html'
    cat=Category.objects.all()
    list=Product.objects.all()

    # Create a paginator to split your products queryset
    paginator = Paginator(list, 8)  # Show 1 contacts per page
    # Get the current page number
    page = request.GET.get('page')

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:  # showing last page
        paginated_queryset = paginator.page(paginator.num_pages)

    context={
        'categories':cat,
        'object':paginated_queryset
    }
    return render(request,template_name,context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'ecom/shop-details.html'
    context_object_name = 'object'

def ProductDeatilFBView(request,slug):
    product=Product.objects.get(slug=slug)








    # TODO related meance use filter with category field

    # related_product=
    template_name = 'ecom/shop-details.html'
    images=Image.objects.filter(Product=product)

    context={
        'object':product,
        'images':images,
    }

# TODO this is thing is only I know What the fuck I did is here
    if request.user.is_authenticated:
        """ USER CART """
        try:
            order=Order.objects.get(user=request.user,is_ordered=False)
            products_in_order=order.products.all()
            product_list=[]
            for i in products_in_order:
                product_list.append(i.product)
                context['product_cart']=i
            print(product_list)
            print(products_in_order)
            if product in product_list:
                context['product_in_cart']=product
                print("This is work")
                print(product)
            print("Product is not")
        except ObjectDoesNotExist:
            messages.warning(request,"Your Cart Is Empty")
            return redirect('index')


    # print(order)
    # print(products_in_order)
    # print(product)

    # if request.user.is_authenticated:
    #     orders=Order.objects.filter(user=request.user,is_ordered=False)
    #     # if orders.products.product.slug==slug



    return render(request,template_name,context)


@login_required
def add_to_cart(request,slug):
    product=get_object_or_404(Product,slug=slug)
    order_product,created=ProductInCart.objects.get_or_create(user=request.user,product=product)

    orders=Order.objects.filter(user=request.user,is_ordered=False)
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

        orders=Order.objects.filter(user=request.user,is_ordered=False)
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

@login_required
def add_single_item_to_cart(request, slug):
    product=get_object_or_404(Product,slug=slug)
    order_product,created=ProductInCart.objects.get_or_create(user=request.user,product=product)

    orders=Order.objects.filter(user=request.user,is_ordered=False)
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

@login_required
def remove_single_item_from_cart(request, slug):
    product=get_object_or_404(Product,slug=slug)
    order_product,created=ProductInCart.objects.get_or_create(user=request.user,product=product)

    orders=Order.objects.filter(user=request.user,is_ordered=False)
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
            orders.delete()
            messages.success(request,f" {product.name}  removed ")
            return redirect("shop-detail",slug=slug)
        else:
            messages.warning(request,  "This product is not in your cart")
            return redirect("shop-detail",slug=slug)
    else:
        messages.warning(request,f' You donot have such product in your cart ')
        return redirect("shop-detail",slug=slug)





def shoppingCart(request):
    products = Order.objects.filter(user=request.user, is_ordered=False)
    save_address_qs = Address.objects.filter(user=request.user, is_save=True)




    if not request.user.is_authenticated:
        messages.warning(request,"Please Register")

    if not products.exists():
        messages.warning(request,"Your Cart Is empty Shop Now")
        return redirect('shop')
    try:
        products=Order.objects.get(user=request.user,is_ordered=False)

        context = {
            'object': products,
        }

        # This is for to redirect save address address
        if save_address_qs.exists():
            redirect_address=save_address_qs[0]
            redirect_address_id=redirect_address.id
            context['redirect_address_id']=redirect_address_id

        return render(request,'ecom/shoping-cart.html',context)
    except ObjectDoesNotExist :
        messages.warning(request, "You do not have an active order")
        redirect('shop')

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
    qs=Product.objects.filter(favourite=request.user,slug=slug)
    if len(qs) > 20:
        messages.warning(request, " Cannot add more than 20")

    if qs.exists():
        messages.warning(request," You already added ")
    else:
        messages.info(request, f" {prod.name} is added")
        prod.favourite.add(request.user)

    return redirect("shop-detail", slug=slug)

@login_required
def remove_from_fav(request,slug):
    prod=get_object_or_404(Product,slug=slug)
    qs=Product.objects.filter(favourite=request.user,slug=slug)
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
        return render(request,'ecom/favourites.html',context)

    except ObjectDoesNotExist:
        messages.warning(request, "You do not have an active order")
        redirect('index')



def category_detail(request,slug):
    cat=get_object_or_404(Category,slug=slug)
    qs=Product.objects.filter(category=cat)
    cats=Category.objects.all()

    # Create a paginator to split your products queryset
    paginator = Paginator(qs, 6)  # Show 1 contacts per page
    # Get the current page number
    page = request.GET.get('page')

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:  # showing last page
        paginated_queryset = paginator.page(paginator.num_pages)


    context={
        'object': paginated_queryset,
        'cat':cat,
        'categories': cats,

    }
    return render(request,'ecom/shop-grid-cat-filter.html',context)



@login_required
def checkoutPage(request):
    save_address=Address.objects.filter(user=request.user,is_save=True)
    context={

    }
    order_qs=Order.objects.filter(user=request.user,is_ordered=False)

    if not order_qs.exists():
        return redirect('cart')

    order=Order.objects.get(user=request.user,is_ordered=False)



    # order_qs=Order.objects.filter(user=request.user)
    # order = order_qs[0]

    if order.get_total_amount() != 0:

        address_form=ChechoutForm()

        if request.POST:
            address_form=ChechoutForm(request.POST or None)
            if address_form.is_valid():
                name=address_form.cleaned_data['name']
                address_1=address_form.cleaned_data['address_1']
                address_2=address_form.cleaned_data['address_2']
                mobile_number=address_form.cleaned_data['mobile_number']
                zipcode=address_form.cleaned_data['zipcode']
                city=address_form.cleaned_data['city']
                is_save=address_form.cleaned_data['is_save']
                payment_option=address_form.cleaned_data['payment_option']

                add_address_from_form=Address(
                    user=request.user,
                    name=name,
                    address_1=address_1,
                    address_2=address_2,
                    mobile_number=mobile_number,
                    zipcode=zipcode,
                    city=city,
                    is_save=is_save,
                )

                if is_save is True:
                    add_address_from_form.save()

                if order.get_total_amount() == 0:
                    messages.warning(request,'Your cart is empty')
                    return redirect('cart')
                if is_save is True:
                    order.address=add_address_from_form
                    order.save()

                if payment_option == 'S':
                    return HttpResponse('Stripe Payment')
                elif payment_option == 'P':
                    return HttpResponse('Paytm')
                elif payment_option == 'C':
                    order.is_ordered=True
                    order.save()
                    transactions = Transaction.objects.create(
                                                            order=order,
                                                            payment_method=payment_option,
                    address_name=name,
                    address_address_1=address_1,
                    address_address_2=address_2,
                    #address_mobile_number_verified=,  AD THIS AFTER THE ADDING PHONE NUMBER FIELD
                    address_mobile_number_2=mobile_number,
                    address_zipcode=zipcode,
                    address_city=city,

                    )
                    transactions.save()
                    messages.success(request,"Your Order Placed Successfully ...!")
                    return redirect('index')
                else:
                    messages.warning(
                        request, "Invalid payment option selected")
                    return redirect('checkout')

        return render(request,'ecom/checkout.html',{
                                                'form':address_form,
                                                'address':save_address,
                                                'order':order,
                                                })
    messages.warning(request,"Your Cart Is Empty")
    return redirect('cart')


#TODO I have work on that
""" THIS IS FOR PREVIOUS ADDRESS """

@login_required
def update_detail_address(request,id):
    save_address=get_object_or_404(Address,id=id)
    addr_user=save_address.user
    if request.user != addr_user:
        return HttpResponse("Restricted  ...!")
    if request.POST:
        address_form=UpdateAddress(request.POST or None,instance=save_address)
        if address_form.is_valid():
            addr=address_form.save(commit=False)
            addr.save()
            save_address=addr
            messages.info(request,f'{save_address.name} is updated')

            # return redirect('update_detail_address',id=id)
            # return redirect('checkout')

            return redirect('save_address')
    form=UpdateAddress(
        initial={
            "name":save_address.name,
            "address_1":save_address.address_1,
            "address_2":save_address.address_2,
            "mobile_number":save_address.mobile_number,
            "zipcode":save_address.zipcode,
            "city":save_address.city,
            "is_save":save_address.is_save,
        }
    )
    context={
        'form':form
    }

    return render(request, 'ecom/checkout-edit-addr.html', context)



""" This is for your previous address """
#TODO USe save address
@login_required
def use_address(request,id):
    save_address=get_object_or_404(Address,id=id)
    order=Order.objects.get(user=request.user,is_ordered=False)
    addr_user=save_address.user
    payment_option_address_form=ChechoutFormPaymentOption()
    if request.user != addr_user:
        return HttpResponse("Restricted  ...!")
    if request.POST:
        payment_option_address_form=ChechoutFormPaymentOption(request.POST or None)
        if payment_option_address_form.is_valid():
            payment_option=payment_option_address_form.cleaned_data['payment_option']

            order.address=save_address
            order.save()

            if payment_option == 'S':
                return HttpResponse('Stripe Payment')
            elif payment_option == 'P':
                return HttpResponse('payment_paytm')
            elif payment_option == 'C':
                order.is_ordered = True
                order.save()
                transactions = Transaction.objects.create(
                    order=order,
                    payment_method=payment_option,
                    address_name=save_address.name,
                    address_address_1=save_address.address_1,
                    address_address_2=save_address.address_2,
                    # address_mobile_number_verified=,  TODO   THIS AFTER THE ADDING PHONE NUMBER FIELD
                    address_mobile_number_2=save_address.mobile_number,
                    address_zipcode=save_address.zipcode,
                    address_city=save_address.city,

                )
                transactions.save()
                messages.success(request, "Your Order Placed Successfully ...!")
                return redirect('index')
            else:
                messages.warning(
                    request, "Invalid payment option selected")
                return redirect('checkout')

    return render(request, 'ecom/checkout-use-addr.html',{
                                                           'form':payment_option_address_form,
                                                           'order':order,
                                                            'save_address':save_address,
                                                          })
@login_required
def delete_address(request,id):
    save_address=get_object_or_404(Address,id=id)
    # order=Order.objects.get(user=request.user,is_ordered=False)
    user=save_address.user
    if user != request.user:
        return HttpResponse("Restricted")
    # if order.address == save_address:
    #     order.address.remove(save_address)
    save_address.delete()
    return redirect('save_address')


@login_required
def order_history(request):
    order_qs=Transaction.objects.filter(order__user=request.user,order__is_ordered=True)

    # order_qs=Order.objects.filter(user=request.user,is_ordered=True)
    # totol_quantity=
    if order_qs.exists():
        context={
            "orders":order_qs,
        }
        return render(request,'ecom/order_history.html',context)
    messages.warning(request,"Your Order History is empty")
    return redirect('cart')

@login_required
def order_history_detailview(request,id=id):
    transaction=Transaction.objects.get(order__user=request.user,order__is_ordered=True,id=id)
    trans_date=transaction.trans_date
    # order=Order.objects.get(id=id)
    order=transaction.order
    # address=order.address
    if order.user != request.user:
        return HttpResponse('Restricted ..!')
    if order is not None:
        context={
            "object":order,
            "trans_date":trans_date,
            "transactions":transaction,
            # 'address':address,
        }
        return render(request,'ecom/order_history_detailview.html',context)
    messages.warning(request,"Your Order History is empty")
    return redirect('cart')

@login_required
def transactions(request):
    transaction=Transaction.objects.filter(order__user=request.user,order__is_ordered=True)
    context={
        'transactions':transaction,
    }
    return render(request,'account/index.html',context)

@login_required
def user_address(request):
    address=Address.objects.filter(user=request.user)
    context={
        'addresses':address,
    }
    return render(request,'ecom/user-address.html',context)

@login_required
def create_address(request):
    address=Address.objects.filter(user=request.user)
    if len(address) > 3:
        messages.warning(request,"You cant create more that three address")
        return redirect('save_address')

    forms=AddressForm()

    if request.method =='POST':
        forms=AddressForm(request.POST or None)
        if forms.is_valid():
            addr=forms.save(commit=False)
            addr.is_save=True
            addr.user=request.user
            addr.save()
            messages.info(request,'Address Is Saved')
            return redirect('index')
    return render(request,'ecom/create-address.html',{'form':forms})
