from django.urls import path, include, re_path
from .views import (
    DashboardView,
    OrderListView,
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('order-list/', OrderListView.as_view(), name="order_list"),
]
