from django import template
from django.db.models import QuerySet
from django.utils.translation import gettext as _

from transaction.models import Purchase

register = template.Library()


@register.filter()
def set_class(value, arg):
    css_classes = arg.split(',')
    value.field.widget.attrs['class'] = ' '.join(css_classes)
    return value


@register.filter()
def add_placeholder(form_field):
    placeholder = ' '.join(list(map(lambda x: x[0].upper() + x[1:], form_field.name.split('_'))))
    form_field.field.widget.attrs['placeholder'] = placeholder
    return form_field


@register.filter()
def get_purchase_queryset_str_repr(value):
    if not isinstance(value, QuerySet) or value.model is not Purchase:
        raise ValueError(_(f'The get_purchase_queryset_str_repr filter only accept Purchase QuerySet!'))
    print(value)
    purchases = []
    for purchase in value:
        purchases.append(f'{purchase.product.name} ({purchase.product.color}) = {purchase.amount}')
    return ',\n'.join(purchases)
