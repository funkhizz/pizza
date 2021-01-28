from django.views.generic import TemplateView
from django.http import HttpResponse

class CartBaseView(TemplateView):
    template_name = "pages/cart-home.html"

def add_to_cart(request):
    pizza_id = request.POST.get('pizza_id')
    quantity = request.POST.get('quantity')
    is_selected = request.POST.getlist('is_selected')
    return HttpResponse(f"{pizza_id}, {quantity}, {is_selected}")

