from django.views.generic import ListView, DetailView
from pizza_online.apps.products.models import Product
from pizza_online.apps.ingredients.models import Ingredient
from .choices import QUANTITY_CHOICES

class ProductListView(ListView):
    template_name = "pages/menu-list.html"
    model = Product


class PizzaDetailView(DetailView):
    template_name = "pages/pizza-detail.html"
    queryset = Product.objects.filter(category="Pizzas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quantity_choices'] = QUANTITY_CHOICES
        context['ingredients'] = Ingredient.objects.all()
        return context
