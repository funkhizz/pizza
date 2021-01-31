from pizza_online.apps.carts.models import CartItem
from pizza_online.apps.ingredients.models import Ingredient


def count_cart_items(request, cart_obj):
    cart_quantity = CartItem.objects.filter(cart=cart_obj).count()
    request.session["cart_items"] = cart_quantity
    return cart_quantity


def add_extra_ingredients(cart_item_id, is_selected, product_obj):
    ingredients = Ingredient.objects.filter(title__in=is_selected)
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.extra_ingredients.set(ingredients)
    extra_ingredients_total_price = 0
    if cart_item.extra_ingredients.all():
        for extra_ingre in cart_item.extra_ingredients.all():
            extra_ingredients_total_price += extra_ingre.price
    cart_item.price = product_obj.price
    cart_item.price += extra_ingredients_total_price
    cart_item.save()


def update_cart(cart_obj):
    cart_obj.refresh_from_db()
    cart_item_qs = CartItem.objects.filter(cart=cart_obj.id)
    cart_obj.total = 0
    for cart_item in cart_item_qs:
        cart_obj.total += cart_item.price
    cart_obj.save()
