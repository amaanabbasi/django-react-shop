from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from core.models import Order, Item, Payment
# Create your views here.


class DashboardView(View):

    def get(self, request):

        orders = Order.objects.all().filter(ordered=True)
        total_orders = orders.count()

        products = Item.objects.all()
        total_products = products.count()

        customers = User.objects.all().filter(is_staff=False)
        total_customers = customers.count()

        payments = Payment.objects.all()
        total_revenue = 0
        for p in payments:
            total_revenue += p.amount

        # Orders that are not received by the customer
        active_orders = orders.filter(received=False)
        total_active_orders = active_orders.count()

        context = {
            "total_active_orders": total_active_orders,
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_products": total_products,
            "total_revenue": total_revenue,


        }
        return render(request, 'dashboard.html', context)


class OrderListView(View):

    def get(self, request):
        orders = Order.objects.all()[::-1]

        context = {
            "orders": orders,
        }
        return render(request, 'order_list_view.html', context)
