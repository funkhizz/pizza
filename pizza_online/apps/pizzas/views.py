from django.views.generic import ListView, DetailView
from pizza_online.apps.pizzas.models import Pizza


class PizzaListView(ListView):
    template_name = "pages/pizza-list.html"
    model = Pizza


class PizzaDetailView(DetailView):
    model = Pizza
    template_name = "pages/pizza-detail.html"
