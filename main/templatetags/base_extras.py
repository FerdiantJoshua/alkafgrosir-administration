import copy

from django import template
from django.db.models import QuerySet
from django.utils.translation import gettext as _

from alkaf_administration.utils import set_field_html_name
from transaction.models import Purchase

register = template.Library()


@register.filter()
def append_class(form_field, arg):
    """Returns the given form_field with appended classes"""
    css_classes = arg.split(',')
    current_class = form_field.field.widget.attrs.get('class') if form_field.field.widget.attrs.get('class') else ''
    form_field.field.widget.attrs['class'] = f'{current_class} {" ".join(css_classes)}'
    return form_field


@register.filter()
def add_placeholder(form_field):
    """Returns the given form_field with appended placeholder from its capizalited-each-word name."""
    placeholder = ' '.join(list(map(lambda x: x[0].upper() + x[1:], form_field.name.split('_'))))
    form_field.field.widget.attrs['placeholder'] = placeholder
    return form_field


@register.filter()
def duplicate_for_autocompleter(form_field, class_):
    """Returns duplicated form_field with new id."""
    new_form_field = copy.deepcopy(form_field)
    new_form_field.field.widget.attrs['id'] = ''
    new_form_field.field.widget.attrs['class'] += f' {class_}'
    set_field_html_name(new_form_field.field, '')
    return new_form_field


@register.filter()
def get_form_model(form):
    """Returns the model of a modelform."""
    return form._meta.model


@register.filter()
def times(n):
    """Returns a iterable range from 1 to n+1"""
    return range(1, n+1)


@register.filter
def dict_key(dict, arg):
    """Returns the given key from a dictionary, with optional default value."""
    arg = arg.split(',')
    key, default = arg[:2] if len(arg) == 2 else (arg[0], None)
    return dict.get(key, default)


@register.filter()
def render_purchase_querysets(value, arg):
    """Returns purchase querysets representation in list with conditional "Detail" button."""
    if not isinstance(value, QuerySet) or value.model is not Purchase:
        raise ValueError(_('The render_purchase_querysets filter only accept Purchase QuerySet!'))
    elif len(arg.split(',')) != 2:
        raise ValueError(_('The render_purchase_querysets filter accepts 2 arguments separated by comma!'))
    # print(f'Value: {value}. Arg: {arg}')
    button_class, data_target_id = arg.split(',')

    purchases = []
    for purchase in value:
        purchase_text = f'{purchase.product.name} ({purchase.product.color}) = {purchase.amount}'
        purchase_text += f'<br><small><i>({purchase.additional_information})</i></small>' if purchase.additional_information else ''
        purchases.append(purchase_text)

    if len(value) > 2:
        purchases = list(map(lambda x: f'<li>{x}</li>', purchases))
        output = f"""
            <div class="d-none">
                <h6 class="font-weight-bold">{len(value)} products:</h6>
                <ol>{''.join(purchases)}</ol>
            </div>
            <button type="button" class="btn btn-secondary btn-sm {button_class}" data-toggle="modal" data-target="#{data_target_id}">
                {len(value)} products
            </button>
        """
    else:
        output = f'{"<br>".join(purchases)}'
    return output
