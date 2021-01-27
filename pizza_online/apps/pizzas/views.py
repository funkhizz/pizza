from django.views.generic import ListView, DetailView
from pizza_online.apps.pizzas.models import Pizza



class PizzaListView(ListView):
    template_name = "pages/pizza-list.html"
    model = Pizza

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pizzas'] = Pizza.objects.all()
        return context

class PizzaDetailView(DetailView):
    model = Pizza
    template_name = "pages/pizza-detail.html"
