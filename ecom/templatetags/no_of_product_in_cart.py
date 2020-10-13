from django import template
from ecom.models import Order

register=template.Library()

@register.filter
def prod_in_cart(user):
    n=Order.objects.filter(user=user,is_ordered=False)
    if n.exists():
        return n[0].products.count()
    return 0