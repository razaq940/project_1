from django import template
from store.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

@register.filter
def status_order_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=True, received=False)
        if qs.exists():
            return qs.count()
    return 0
