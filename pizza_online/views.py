from django.views.generic import TemplateView
from pizza_online.apps.pizzas.models import Pizza


class BaseView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["pizzas"] = Pizza.objects.all()
        return context





