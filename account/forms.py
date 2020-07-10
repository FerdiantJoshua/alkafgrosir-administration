from django.contrib.auth.forms import AuthenticationForm

from alkaf_administration.utils import set_fields_css_class


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        set_fields_css_class(self.fields)
