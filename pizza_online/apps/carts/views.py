from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from pizza_online.apps.products.models import Product
from .models import CartItem, Cart


class CartHomeBaseView(TemplateView):
    template_name = "pages/cart-home.html"

    def get(self, request, *args, **kwargs):
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cartItems = CartItem.objects.filter(cart=cart_obj.id)
        context = {"cart_items": cartItems, "cart": cart_obj}
        return render(request, self.template_name, context)


def add_to_cart(request):
    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity"))
    is_selected = request.POST.getlist("is_selected")
    if product_id:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("carts:cart-home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart_obj, product=product_obj
        )
        cart_item.quantity += quantity
        cart_item.line_total = product_obj.price * cart_item.quantity
        cart_obj.refresh_from_db()
        cart_obj.total += product_obj.price * quantity
        cart_item.save()
        cart_obj.save()
        cart_quantity = 0
        all_items = CartItem.objects.filter(cart=cart_obj)
        for item in all_items:
            cart_quantity += item.quantity
        request.session["cart_items"] = cart_quantity
    return redirect("carts:cart-home")
