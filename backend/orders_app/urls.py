from django.urls import path
from .views import (
    OrderCreateView,
    OrderListView,
    OrderDetailView,
    OrderCancelView
)

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'), # GET /api/orders/
    path('new/', OrderCreateView.as_view(), name='order-create'), # POST /api/orders/new/
    path('<int:id>/', OrderDetailView.as_view(), name='order-detail'), # GET /api/orders/<id>/
    path('<int:id>/cancel/', OrderCancelView.as_view(), name='order-cancel'), # PATCH /api/orders/<id>/cancel/
]
