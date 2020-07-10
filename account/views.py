from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from account.forms import LoginForm
from alkaf_administration.utils import add_invalid_css_class_to_form


class EnhancedLoginView(LoginView):
    model = User
    form_class = LoginForm
    redirect_authenticated_user = True

    def __init__(self, *args, **kwargs):
        super(EnhancedLoginView, self).__init__(*args, **kwargs)

    @add_invalid_css_class_to_form
    def form_invalid(self, form):
        return super().form_invalid(form)