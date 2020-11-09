from django import template
from ecom.models import Order,Product

register=template.Library()

@register.filter
def prod_in_cart(user):
    n=Order.objects.filter(user=user,is_ordered=False)
    if n.exists():
        return n[0].products.count()
    return 0

@register.filter
def prod_in_favourite_list(user):
    n=Product.objects.filter(favourite=user)
    if n.exists():
        return n.count()
    return 0
@register.filter
def total_bill_amount(user):
    n=Order.objects.filter(user=user,is_ordered=False)
    if n.exists():
        return n[0].get_total_amount()
    return 0