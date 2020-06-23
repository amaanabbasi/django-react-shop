from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
import random
import string

CATEGORY_CHOICES = (
    ('DR', 'Drink'),
    ('DO', 'Deals & Offers'),
    ('DI', 'Dairy Items'),
    ('FV', 'Fruits & Vegetables'),
    ('GR', 'Groceries'),
    ('HS', 'Household Supplies'),
    ('BP', 'Beauty & Personal Care'),
    ('OT', 'Others'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def upload_location(instance, filename):

    #filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    # PostModel = instance.__class__
    # new_id = PostModel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """

    # filebase, _ = filename.split(".")
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=24))
    return "products/%s.jpg" % (res)


class ImageUploads(models.Model):
    image = models.ImageField(
        upload_to=upload_location, blank=False, null=False)


class Item(models.Model):
    title = models.CharField(max_length=100)
    sku = models.CharField(max_length=8, validators=[
                           MinLengthValidator(8)], unique=True)
    upc = models.CharField(max_length=12, validators=[
                           MinLengthValidator(12)], unique=True, blank=True, null=True)
    date_updated = models.DateTimeField(
        auto_now=True, blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    # def save(self, *args, **kwargs):
    #     # call the compress function
    #     # new_image = compress(self.image)
    #     # set self.image to new_image
    #     self.image = image
    #     # save
    #     super().save(*args, **kwargs)


class Variation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # size

    class Meta:
        unique_together = (
            ('item', 'name')
        )

    def __str__(self):
        return self.name


class ItemVariation(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)  # S, M, L
    attachment = models.ImageField(blank=True)

    class Meta:
        unique_together = (
            ('variation', 'value')
        )

    def __str__(self):
        return self.value


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_variations = models.ManyToManyField(ItemVariation)
    quantity = models.IntegerField(default=1)
    # Should not be blank, itemPrice at time of purchase
    purchase = models.FloatField(blank=True, null=True)
    # Since it can change at later point of time it should be saved

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


# class DeliveredOrder(models.Model):


"""
Edit: Another thing to consider is having a built in way to distinguish orders, customers, 
etc. e.g. customers always start with 10, orders always start 
with 20, vendors always start with 30, etc.
"""


class ItemPrice(models.Model):
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    price = models.FloatField(blank=True, null=True)  # change blank and null
    date_changed = models.DateTimeField(auto_now=True, blank=True, null=True)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(
        max_length=20, blank=True, null=True, unique=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    # Check this
    ordered_date = models.DateTimeField()
    # When the payment is made it becomes True
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    refund_refused = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
        6.1 
            - refund_request When a user requests for a refund on an order.
            - refund_granted It is set to true by the admin after verfication of the request.
            - refuned_refused It is set to true by the admin if the refund cannot be issued.  
              and  if true that means now no more refund request can be initiated 
               on this order.
 
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def get_status(self):
        status = self.ordered + self.being_delivered + self.received
        if status == 0:
            return "Not Ordered"
        if status == 1:
            return "Ordered"
        elif status == 2:
            return "Sent for delivery"
        elif status == 3:
            return "Delivered"
        # LAter add refund

    def get_absolute_url(self):
        return reverse("dashboard:product_detail", kwargs={
            'slug': self.slug
        })


class Shipping(models.Model):
    pass


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_full_address(self):
        return str(self.apartment_address) + ", " + str(self.street_address) + ", " + str(self.zip)

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
