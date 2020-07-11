from django.urls import path

from . import views

app_name = 'transaction'
urlpatterns = [
    path('', views.MainTransactionView.as_view(), name='index'),
]
