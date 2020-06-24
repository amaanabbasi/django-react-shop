from django.conf import settings
import logging
from django.urls import reverse
from dashboard.forms import ItemForm, ImageUploads
import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View
from django.views.generic import ListView, DetailView
from core.models import Order, Item, Payment, ImageUploads, Refund, ItemOrdered
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
# Or ItemCreateView
logger = logging.getLogger(__name__)


class ProductListView(PermissionRequiredMixin, ListView):
    permission_required = 'is_staff'
    model = Item
    # paginate_by = 10
    template_name = "product_list.html"


@staff_member_required
def product_create_view(request):
    # create objects
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # import pdb
            # pdb.set_trace()
            messages.add_message(request, messages.INFO,
                                 'Product Added Successfully')
            return HttpResponseRedirect(reverse('core:home'))
        else:
            print(form)
    else:
        form = ItemForm()

    template_name = 'item_create_form.html'
    context = {'form': form}
    return render(request, template_name, context)


@staff_member_required
def product_update_view(request, id):
    obj = get_object_or_404(Item, id=id)
    form = ItemForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,
                                 'Product Updated Successfully')
            return HttpResponseRedirect(reverse('dashboard:product_list'))

    template_name = 'item_update_form.html'
    context = {'form': form,
               'product_id': id}
    return render(request, template_name, context)


class DashboardView(PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request):

        # Items or stock
        stock_items = Item.objects.all()
        total_stock_items = stock_items.count()

        # Order details
        orders = Order.objects.all().filter(ordered=True, refund_granted=False)
        total_orders = orders.count()

        # Order details about 24 hours
        time_24_hours_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        past_24_hours_orders = orders.filter(
            ordered_date__gte=time_24_hours_ago).filter(ordered=True)
        total_past_24_hours_orders = past_24_hours_orders.count()

        revenue_past_24_hours_orders = 0
        for order in past_24_hours_orders:
            revenue_past_24_hours_orders += order.get_total_ordered()

        average_revenue_24_hours = 0
        try:
            average_revenue_24_hours = revenue_past_24_hours_orders/total_past_24_hours_orders
        except Exception as err:
            logging.debug(str(err) + ": DashboardView")

        products = Item.objects.all()
        total_products = products.count()

        # Customer detail
        customers = User.objects.all().filter(is_staff=False)
        total_customers = customers.count()

        # Customer details about 24 hours (New Customers)
        customers_time_24_hours_ago = customers.filter(
            date_joined__gte=time_24_hours_ago)
        total_customers_time_24_hours_ago = customers_time_24_hours_ago.count()

        # Total Revenue
        payments = Payment.objects.all()
        total_revenue = 0
        for p in payments:
            total_revenue += p.amount
        try:
            average_total_revenue = total_revenue // total_orders
        except ZeroDivisionError:
            logging.error(str(err) + ": DashboardView")

        # Active Orders - Orders that are not received by the customer
        active_orders = orders.filter(received=False)
        total_active_orders = active_orders.count()

        context = {
            "total_active_orders": total_active_orders,
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_products": total_products,
            "total_revenue": total_revenue,

            "total_past_24_hours_orders": total_past_24_hours_orders,
            "revenue_past_24_hours_orders": revenue_past_24_hours_orders,
            "average_revenue_24_hours": average_revenue_24_hours,
            "average_total_revenue": average_total_revenue,

            "total_stock_items": total_stock_items,
            "total_customers_time_24_hours_ago": total_customers_time_24_hours_ago,

        }

        return render(request, 'dashboard.html', context)


class OrderListView(PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request):

        orders = Order.objects.all().filter(
            ordered=True, refund_requested=False)[::-1]

        context = {
            "orders": orders,
        }
        return render(request, 'order_list_view.html', context)

    def post(self, request):
        """
        0 -> Not ordered but in cart
        1 -> Ordered
        2 -> Sent for delivery
        3 -> delivered

        Check models for 'Item' for more info.
        """

        order_ids = request.POST.getlist("order_id")
        order_ids = list(map(int, order_ids))

        update_status_for_orders = int(request.POST['status'])

        orders = Order.objects.filter(id__in=order_ids)

        if update_status_for_orders == 2:
            orders.update(being_delivered=True)

        elif update_status_for_orders == 3:
            orders.update(received=True)

        orders = Order.objects.all().filter(ordered=True)[::-1]

        context = {
            "orders": orders,
        }

        return render(request, 'order_list_view.html', context)


class OrderDetailView(PermissionRequiredMixin, View):
    permission_required = 'is_staff'

    def get(self, request, id):

        order = Order.objects.get(id=id)

        context = {
            "order": order,
        }
        return render(request, 'order_detail_view.html', context)

    def post(self, request):
        """
        0 -> Not ordered but in cart
        1 -> Ordered
        2 -> Sent for delivery
        3 -> delivered

        Check models for 'Item' for more info.
        """

        order_ids = request.POST.getlist("order_id")
        order_ids = list(map(int, order_ids))

        update_status_for_orders = int(request.POST['status'])

        orders = Order.objects.filter(id__in=order_ids)

        if update_status_for_orders == 2:
            orders.update(being_delivered=True)

        elif update_status_for_orders == 3:
            orders.update(received=True)

        orders = Order.objects.all().filter(ordered=True)[::-1]

        context = {
            "order": orders,
        }

        return render(request, 'order_detail_view.html', context)


class RefundListView(PermissionRequiredMixin, View):
    """
    Refund requests sent by the customers appear here. 
    The admin can grant or deny a refund request as per his/her will.

    When a grant request is made on a refund an api request is sent to stripe
    with stripe_charge_id, stripe_charge_id is the same id that was created when the payment
    for this order was done by the customer. Stripe will automatically stop repeated refund request
    on the same order. This request is irreversible.

    When a Deny request is made the order is denied refund. 
    """
    permission_required = 'is_staff'

    def get(self, request):

        refund_list = Refund.objects.all()[::-1]

        context = {
            "refund_list": refund_list,
        }
        return render(request, 'refund_view.html', context)

    def post(self, request):
        refund_id = int(request.POST.get("refund_id"))
        order_ref_code = request.POST.get("order_ref_code")
        update_status_for_refund = int(request.POST['status'])
        # refund = get_object_or_404(Refund, id=refund_id)

        order = get_object_or_404(Order, ref_code=order_ref_code)
        stripe_charge_id = order.payment.stripe_charge_id

        if update_status_for_refund == 1:
            try:
                refund_stripe = stripe.Refund.create(
                    charge=stripe_charge_id,
                )
                order.refund_granted = True
                # refund.save()
                order.save()
            except Exception as err:
                messages.warning(request, f"Message: {err.code}")
                return HttpResponseRedirect(reverse('dashboard:refund_list'))
            messages.info(request, "Refund Granted")
            return HttpResponseRedirect(reverse('dashboard:refund_list'))
        elif update_status_for_refund == -1:
            if order.refund_granted == True:
                messages.warning(request, "Refund has already occured.")
                return HttpResponseRedirect(reverse('dashboard:refund_list'))
            order.refund_refused = True
            order.save()
            messages.info(request, "Refund Not Granted")
            return HttpResponseRedirect(reverse('dashboard:refund_list'))
