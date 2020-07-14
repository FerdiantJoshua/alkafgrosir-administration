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
def render_purchase_querysets(value, arg):
    if not isinstance(value, QuerySet) or value.model is not Purchase:
        raise ValueError(_('The render_purchase_querysets filter only accept Purchase QuerySet!'))
    elif len(arg.split(',')) != 2:
        raise ValueError(_('The render_purchase_querysets filter accepts 2 arguments separated by comma!'))
    # print(f'Value: {value}. Arg: {arg}')
    button_class, data_target_id = arg.split(',')

    purchases = []
    for purchase in value:
        purchases.append(f'{purchase.product.name} ({purchase.product.color}) = {purchase.amount}')

    if len(value) > 2:
        purchases = list(map(lambda x: f'<li>{x}</li>', purchases))
        output = f'''
            <div class="d-none">
                <h6 class="font-weight-bold">{len(value)} products:</h6>
                <ol>{''.join(purchases)}</ol>
            </div>
            <button type="button" class="btn btn-primary btn-sm {button_class}" data-toggle="modal" data-target="#{data_target_id}">
                {len(value)} products
            </button>
        '''
    else:
        output = f'{"<br>".join(purchases)}'
    return output
