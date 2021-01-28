from django.urls import path, include
from .views import CartBaseView, add_to_cart

app_name = "carts"

urlpatterns = [
    path("", CartBaseView.as_view(), name="cart-home"),
    path("add_to_cart/", add_to_cart, name="add_to_cart"),
]
