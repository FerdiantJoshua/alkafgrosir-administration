from django import template

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
