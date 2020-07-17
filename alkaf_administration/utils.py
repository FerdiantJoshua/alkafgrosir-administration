def set_fields_css_class(fields):
    for key in fields:
        placeholder = ' '.join(list(map(lambda x: x[0].upper() + x[1:], key.split('_'))))
        fields[key].widget.attrs.update({'class': 'form-control', 'placeholder': placeholder})


def add_invalid_css_class_to_form(func):
    def wrapper(*args, **kwargs):
        form = args[1]
        objects = form.fields if form.non_field_errors() else form.errors
        for key in objects:
            field = form.fields.get(key)
            field.widget.attrs.update({'class': field.widget.attrs['class'] + ' is-invalid'})
        return func(*args, **kwargs)
    return wrapper


def set_field_html_name(cls, new_name):
    """
    This creates wrapper around the normal widget rendering,
    allowing for a custom field name (new_name).
    """
    old_render = cls.widget.render
    def _widget_render_wrapper(name, value, attrs=None, renderer=None):
        return old_render(new_name, value, attrs, renderer)
    cls.widget.render = _widget_render_wrapper
