from django.urls import path, include
from .views import ProductListView, PizzaDetailView

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="menu-list"),
    path("pizzas/<slug:slug>/", PizzaDetailView.as_view(), name="pizza-detail"),
]
