from django.urls import path, include
from .views import add_to_cart, CartHomeBaseView

app_name = "carts"

urlpatterns = [
    path("", CartHomeBaseView.as_view(), name="cart-home"),
    path("add_to_cart/", add_to_cart, name="add_to_cart"),
]
