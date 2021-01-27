from django.views.generic import TemplateView, DetailView
from pizza_online.apps.pizzas.models import Pizza

class PizzaDetailView(DetailView):
    model = Pizza
    template_name = "detail.html"
