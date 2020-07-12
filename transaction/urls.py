from django.urls import path

from . import views

app_name = 'transaction'
urlpatterns = [
    path('', views.TransactionListView.as_view(), name='list_transaction'),
    path('create/', views.TransactionCreateView.as_view(), name='create_transaction'),
    path('<int:pk>', views.TransactionEditView.as_view(), name='edit_transaction'),
    path('delete/<int:pk>', views.TransactionDeleteView.as_view(), name='delete_transaction'),
]
