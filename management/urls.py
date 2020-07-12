from django.urls import path

from . import views

app_name = 'management'
urlpatterns = [
    path('main/', views.ManagementMainView.as_view(), name='main'),
    path('marketplace/create', views.MarketplaceCreateView.as_view(), name='create_marketplace'),
    path('marketplace/', views.MarketplaceListView.as_view(), name='list_marketplace'),
    path('marketplace/<int:pk>', views.MarketplaceEditView.as_view(), name='edit_marketplace'),
    path('marketplace/delete/<int:pk>', views.MarketplaceDeleteView.as_view(), name='delete_marketplace'),
    # path('add_customer/', views.MainTransactionView.as_view(), name='add_customer'),
    # path('add_city/', views.MainTransactionView.as_view(), name='add_city'),
    # path('add_courier/', views.MainTransactionView.as_view(), name='add_courier'),
    # path('add_product_variation/', views.MainTransactionView.as_view(), name='add_product_variation'),
]
