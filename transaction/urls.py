from django.urls import path

from . import views

app_name = 'transaction'
urlpatterns = [
    path('', views.TransactionListView.as_view(), name='list_transaction'),
    path('export/', views.export_transaction, name='export_transaction'),
    path('update-status/', views.update_status_is_packed, name='update_status_transaction'),
    path('create/', views.TransactionCreateView.as_view(), name='create_transaction'),
    path('<int:pk>', views.TransactionEditView.as_view(), name='edit_transaction'),
    path('delete/<int:pk>', views.TransactionDeleteView.as_view(), name='delete_transaction'),
    path('duplicate/', views.TransactionDuplicateView.as_view(), name='duplicate_transaction'),
]
