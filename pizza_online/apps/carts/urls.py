from django.urls import path, include
from .views import add_to_cart, CartHomeBaseView, remove_from_cart, update_item

app_name = "carts"

urlpatterns = [
    path("", CartHomeBaseView.as_view(), name="cart-home"),
    path("add_to_cart/", add_to_cart, name="add_to_cart"),
    path("remove_from_cart/", remove_from_cart, name="remove_from_cart"),
    path("update_item/", update_item, name="update_item")
]
