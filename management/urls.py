from django.urls import path

from . import views

app_name = 'management'
urlpatterns = [
    path('main/', views.ManagementMainView.as_view(), name='main'),

    path('marketplace/create', views.MarketplaceCreateView.as_view(), name='create_marketplace'),
    path('marketplace/', views.MarketplaceListView.as_view(), name='list_marketplace'),
    path('marketplace/<int:pk>/', views.MarketplaceEditView.as_view(), name='edit_marketplace'),
    path('marketplace/delete/<int:pk>/', views.MarketplaceDeleteView.as_view(), name='delete_marketplace'),

    path('customer/create', views.CustomerCreateView.as_view(), name='create_customer'),
    path('customer/', views.CustomerListView.as_view(), name='list_customer'),
    path('customer/<int:pk>/', views.CustomerEditView.as_view(), name='edit_customer'),
    path('customer/delete/<int:pk>/', views.CustomerDeleteView.as_view(), name='delete_customer'),

    path('city/create', views.CityCreateView.as_view(), name='create_city'),
    path('city/', views.CityListView.as_view(), name='list_city'),
    path('city/<int:pk>/', views.CityEditView.as_view(), name='edit_city'),
    path('city/delete/<int:pk>/', views.CityDeleteView.as_view(), name='delete_city'),

    path('courier/create', views.CourierCreateView.as_view(), name='create_courier'),
    path('courier/', views.CourierListView.as_view(), name='list_courier'),
    path('courier/<int:pk>/', views.CourierEditView.as_view(), name='edit_courier'),
    path('courier/delete/<int:pk>/', views.CourierDeleteView.as_view(), name='delete_courier'),

    path('product/create', views.ProductCreateView.as_view(), name='create_product'),
    path('product/', views.ProductListView.as_view(), name='list_product'),
    path('product/<int:pk>', views.ProductEditView.as_view(), name='edit_product'),
    path('product/delete/<int:pk>', views.ProductDeleteView.as_view(), name='delete_product'),
]
