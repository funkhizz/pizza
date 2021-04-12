import math

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from pizza_online.apps.carts.models import Cart, CartItem
from pizza_online.utils import unique_order_id_generator
from pizza_online.apps.billing.models import BillingProfile
from pizza_online.apps.addresses.models import Address
from pizza_online.apps.products.models import Product


ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("refunded", "Refunded"),
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True,
            status="created",
        )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile, cart=cart_obj
            )
            created = True
        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(
        BillingProfile, on_delete=models.CASCADE, blank=True, null=True
    )
    shipping_address = models.ForeignKey(
        Address,
        related_name="shipping_address",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=120, default="created", choices=ORDER_STATUS_CHOICES
    )
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        total = self.total
        new_total = float(total)
        if new_total < 0:
            return False
        elif billing_profile and shipping_address and new_total > 0:
            return True
        return False

    def order_paid(self):
        if self.check_done():
            print("hey")
            self.status = "paid"
            self.save()
        return self.status


@receiver(pre_save, sender=Order)
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(
        billing_profile=instance.billing_profile
    )
    if qs.exists():
        qs.update(active=False)


@receiver(post_save, sender=Cart)
def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart_id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


@receiver(post_save, sender=Order)
def post_save_order_products(sender, instance, *args, **kwargs):
    if instance.status == "paid":
        cartitems = CartItem.objects.filter(cart=instance.cart)
        for item in cartitems:
            product = Product.objects.get(id=item.product.id)
            product.item_sold += item.quantity
            product.save()
