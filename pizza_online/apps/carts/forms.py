from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from django.utils.html import mark_safe
from django.contrib.auth.password_validation import (
    password_validators_help_text_html,
    validate_password,
)
from crispy_forms.layout import (
    Layout,
    Field,
    ButtonHolder,
    Submit,
    Div,
    Row,
    HTML,
)

from pizza_online.apps.addresses.models import Address


class BillingForm(forms.ModelForm):
    email = forms.EmailField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(BillingForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy("carts:cart-checkout")

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit("save", "Pay and get order"))

    class Meta:
        model = Address
        fields = [
            "first_name",
            "last_name",
            "email",
            "company",
            "address_1",
            "address_2",
            "city",
            "country",
            "post_code",
            "phone",
        ]
