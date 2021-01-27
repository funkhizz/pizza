from django.urls import path, include
from .views import PizzaListView, PizzaDetailView

app_name = "pizzas"

urlpatterns = [
    path("", PizzaListView.as_view(), name="pizza-list"),
    path("<slug:slug>/", PizzaDetailView.as_view(), name="pizza-detail"),
]
