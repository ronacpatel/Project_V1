
from django.urls import path
from .views import ReceiptListCreateView

urlpatterns = [
    path('receipts/', ReceiptListCreateView.as_view(), name='receipt-list-create'),
]
