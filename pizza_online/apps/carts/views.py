from django.views.generic import TemplateView
from django.shortcuts import redirect, render

from crispy_forms.layout import HTML, Field

from pizza_online.apps.products.models import Product
from pizza_online.apps.carts.models import CartItem, Cart
from pizza_online.apps.ingredients.models import Ingredient
from pizza_online.apps.products.choices import QUANTITY_CHOICES
from pizza_online.apps.billing.models import BillingProfile
from pizza_online.apps.addresses.models import Address
from pizza_online.apps.orders.models import Order

from .utils import add_extra_ingredients, update_cart, count_cart_items
from .forms import BillingForm


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


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if cart_created and CartItem.objects.filter(cart=cart_obj.id).count() == 0:
        return redirect("carts:cart-home")
    cartItems = CartItem.objects.filter(cart=cart_obj.id)

    billing_form = BillingForm()
    if request.user.is_authenticated:
        billing_form.helper.layout.pop(2)
    if request.method == "GET":
        context = {
            "cart_items": cartItems,
            "cart": cart_obj,
            "billing_form": billing_form,
        }
        return render(request, "pages/checkout.html", context)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        company = request.POST.get("company", "")
        address_1 = request.POST.get("address_1")
        address_2 = request.POST.get("address_2", "")
        city = request.POST.get("city")
        country = request.POST.get("country")
        post_code = request.POST.get("post_code")
        phone = request.POST.get("phone", "")
        order_obj = None
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        email = request.POST.get("email")
        if email:
            request.session["email_id"] = email
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
            request
        )
        address = Address.objects.create(
            billing_profile=billing_profile,
            first_name=first_name,
            last_name=last_name,
            company=company,
            address_1=address_1,
            address_2=address_2,
            city=city,
            country=country,
            post_code=post_code,
            phone=phone,
        )
        if billing_profile is not None:
            order_obj, order_obj_created = Order.objects.new_or_get(
                billing_profile, cart_obj
            )
            if address:
                order_obj.shipping_address = address
                order_obj.save()
        cartItems = CartItem.objects.filter(cart=cart_obj.id)

        context = {
            "billing_profile": billing_profile,
            "order_number": order_obj,
            "cart_items": cartItems,
            "address": address,
        }
        # TODO: write for succesful payment
        # remove sessions

        return render(request, "pages/check-data.html", context)


# def CheckoutDone(request):
#     billing_form = BillingForm(request.POST)
#     print(billing_form)
#     return render(request, "pages/checkout-done.html", context={})


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
                add_extra_ingredients(cart_item.id, is_selected, product_obj)
        else:
            add_extra_ingredients(cart_item_id, is_selected, product_obj)
        update_cart(cart_obj)
        count_cart_items(request, cart_obj)
    return redirect("carts:cart-home")


def remove_from_cart(request):
    cart_item_id = request.POST.get("cart_item_id")
    cart_id = request.POST.get("cart_id")
    cart_obj = Cart.objects.get(id=cart_id)
    if cart_item_id:
        CartItem.objects.get(id=cart_item_id).delete()
        update_cart(cart_obj)
        cart_items = count_cart_items(request, cart_obj)
        if cart_items:
            return redirect("carts:cart-home")
    return redirect("products:menu-list")
