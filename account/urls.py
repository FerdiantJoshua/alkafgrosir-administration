from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.EnhancedLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
