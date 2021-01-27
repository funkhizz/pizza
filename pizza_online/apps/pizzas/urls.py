from django.urls import path, include
from .views import PizzaDetailView

app_name = "pizzas"

urlpatterns = [
    path("<slug:slug>/", PizzaDetailView.as_view(), name="pizza_detail"),
]
