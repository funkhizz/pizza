from django.views.generic import TemplateView
from django.shortcuts import redirect, render

from pizza_online.apps.products.models import Product

from pizza_online.apps.carts.models import CartItem, Cart
from pizza_online.apps.ingredients.models import Ingredient
from pizza_online.apps.products.choices import QUANTITY_CHOICES


def update_item(request):
    cart_item_id = request.POST.get("cart_item_id")
    cart_item = CartItem.objects.get(id=cart_item_id)
    ingredients = Ingredient.objects.all()
    context = {
        "cart_item": cart_item,
        "ingredients": ingredients,
        "quantity_choices": QUANTITY_CHOICES,
    }
    return render(request, "pages/update_item.html", context)


class CartHomeBaseView(TemplateView):
    template_name = "pages/cart-home.html"

    def get(self, request, *args, **kwargs):
        cart_quantity = 0
        if request.session.get("cart_items", False):
            cart_quantity = request.session.get("cart_items")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cartItems = CartItem.objects.filter(cart=cart_obj.id)
        context = {
            "cart_items": cartItems,
            "cart": cart_obj,
            "cart_quantity": cart_quantity,
        }
        if cartItems:
            return render(request, self.template_name, context)
        return redirect("products:menu-list")


def add_to_cart(request):
    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity")
    is_selected = request.POST.getlist("is_selected")
    cart_item_id = request.POST.get("cart_item_id")
    if product_id:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("carts:cart-home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if not cart_item_id:
            for i in range(int(quantity)):
                cart_item = CartItem.objects.create(
                    cart=cart_obj,
                    product=product_obj,
                    quantity=1,
                    price=product_obj.price,
                )
                add_extra_ingredients(cart_item.id, is_selected)
            cart_obj.refresh_from_db()
            cart_obj.total += product_obj.price
            cart_obj.save()
        else:
            add_extra_ingredients(cart_item_id, is_selected)
        count_cart_items(request, cart_obj)
    return redirect("carts:cart-home")


def remove_from_cart(request):
    cart_item_id = request.POST.get("cart_item_id")
    cart_id = request.POST.get("cart_id")
    if cart_item_id:
        cart_item = CartItem.objects.get(id=cart_item_id).delete()
        cart_items = CartItem.objects.filter(cart=cart_id)
        total = 0
        for cart_item in cart_items:
            total += cart_item.product.price
        cart_obj = Cart.objects.get(id=cart_id)
        cart_obj.total = total
        cart_obj.save()
        count_cart_items(request, cart_obj)
        if cart_items:
            return redirect("carts:cart-home")
    return redirect("products:menu-list")


def count_cart_items(request, cart_obj):
    cart_quantity = CartItem.objects.filter(cart=cart_obj).count()
    request.session["cart_items"] = cart_quantity


def add_extra_ingredients(cart_item_id, is_selected):
    ingredients = Ingredient.objects.filter(title__in=is_selected)
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.extra_ingredients.set(ingredients)
    total_sum = 0
    if cart_item.extra_ingredients.all():
        for extra_ingre in cart_item.extra_ingredients.all():
            total_sum += extra_ingre.price
    cart_item.price += total_sum
    cart_item.save()
