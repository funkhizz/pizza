from django.views.generic import ListView, DetailView
from pizza_online.apps.pizzas.models import Pizza
from pizza_online.apps.ingredients.models import Ingredient
from .quantity_choices import quantity_choices

class PizzaListView(ListView):
    template_name = "pages/pizza-list.html"
    model = Pizza


class PizzaDetailView(DetailView):
    model = Pizza
    template_name = "pages/pizza-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quantity_choices'] = quantity_choices
        context['ingredients'] = Ingredient.objects.all()
        return context
