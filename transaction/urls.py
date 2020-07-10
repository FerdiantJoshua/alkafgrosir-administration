from django.urls import path

from . import views

app_name = 'transaction'
urlpatterns = [
    path('', views.MainTransactionView.as_view(), name='index'),
    path('add_marketplace/', views.MainTransactionView.as_view(), name='add_marketplace'),
    path('add_customer/', views.MainTransactionView.as_view(), name='add_customer'),
    path('add_city/', views.MainTransactionView.as_view(), name='add_city'),
    path('add_courier/', views.MainTransactionView.as_view(), name='add_courier'),
    path('add_product_variation/', views.MainTransactionView.as_view(), name='add_product_variation'),
]
