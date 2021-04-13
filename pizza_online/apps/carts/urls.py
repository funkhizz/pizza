from django.urls import path
from .views import (
    add_to_cart,
    CartHomeBaseView,
    remove_from_cart,
    update_item,
    checkout_home,
    # CheckoutDone,
)

app_name = "carts"

urlpatterns = [
    path("", CartHomeBaseView.as_view(), name="cart-home"),
    path("checkout/", checkout_home, name="cart-checkout"),
    # path("checkout-done/", CheckoutDone, name="cart-checkout-done"),
    path("add_to_cart/", add_to_cart, name="add_to_cart"),
    path("remove_from_cart/", remove_from_cart, name="remove_from_cart"),
    path("update_item/", update_item, name="update_item"),
]
