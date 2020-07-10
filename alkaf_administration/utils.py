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
