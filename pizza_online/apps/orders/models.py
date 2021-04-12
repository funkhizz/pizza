from django.db import models
from pizza_online.apps.carts.models import Cart, CartItem
from pizza_online.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save
from pizza_online.apps.billing.models import BillingProfile
