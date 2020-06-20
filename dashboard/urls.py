from django.urls import path, include, re_path
from .views import (
    DashboardView,
    OrderListView,
    OrderDetailView,
    product_create_view,
    product_update_view,
    ProductListView,
    RefundListView,
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('order-list/', OrderListView.as_view(), name="order_list"),
    path('refund-list/', RefundListView.as_view(), name="refund_list"),
    path('<id>/order-detail/', OrderDetailView.as_view(), name="order_detail"),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('add-product/', product_create_view, name="add_product"),
    path('<id>/update-product/', product_update_view, name="product_update"),
]
