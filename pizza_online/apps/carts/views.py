from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from pizza_online.apps.products.models import Product
from .models import CartItem, Cart


class CartHomeBaseView(TemplateView):
    template_name = "pages/cart-home.html"

    def get(self, request, *args, **kwargs):
        if request.session.get("cart_items", False):
            cart_quantity = request.session.get("cart_items")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cartItems = CartItem.objects.filter(cart=cart_obj.id)
        print(cart_quantity)
        context = {
            "cart_items": cartItems,
            "cart": cart_obj,
            "cart_quantity": cart_quantity,
        }
        if cartItems == 0:
            return redirect("products:menu-list")
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
        for i in range(quantity):
            cart_item = CartItem.objects.create(
                cart=cart_obj, product=product_obj, quantity=1
            )
            cart_obj.refresh_from_db()
            cart_obj.total += product_obj.price * quantity
            cart_item.save()
            cart_obj.save()

        cart_quantity = 0
        all_items = CartItem.objects.filter(cart=cart_obj)
        for item in all_items:
            cart_quantity += item.quantity
        count_cart_items(request, cart_obj)
    return redirect("carts:cart-home")


def remove_from_cart(request):
    cart_item_id = request.POST.get("cart_item_id")
    cart_id = request.POST.get("cart_id")
    if cart_item_id:
        cart_item = CartItem.objects.get(id=cart_item_id).delete()
        cart_items = CartItem.objects.filter(cart=cart_id)
        print(cart_items)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price
        cart_obj = Cart.objects.get(id=cart_id)
        print(cart_items)
        if cart_items:
            cart_obj.total = total
            cart_obj.save()
            count_cart_items(request, cart_obj)
            return redirect("carts:cart-home")
    return redirect("products:menu-list")


def count_cart_items(request, cart_obj):
    cart_quantity = 0
    all_items = CartItem.objects.filter(cart=cart_obj)
    for item in all_items:
        cart_quantity += item.quantity
    request.session["cart_items"] = cart_quantity
