from django.utils.translation import gettext as _
from django.conf import settings
from django.views.generic import UpdateView, TemplateView
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from django_registration import signals
from django_registration.views import RegistrationView as BaseRegistrationView
from .utils import ProtectedView

from .models import User
from .forms import LoginForm, CustomUserEditForm, CustomUserCreationForm


class HomeView(ProtectedView, TemplateView):
    template_name = "pages/users/home.html"


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_or_register(request):
    """
    Router page to display login and register forms on same page.
    Form processing is handled by each separate view.
    """
    login_form = LoginForm()
    registration_form = CustomUserCreationForm()
    template_name = "registration/login_or_register.html"

    if request.method == "POST":
        redirect_to = request.POST.get(
            "next",
            request.GET.get("next"),
        )
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            # Okay, security check complete. Sign the user in.
            auth_login(request, login_form.get_user())
            if not redirect_to:
                redirect_to = reverse_lazy(settings.LOGIN_REDIRECT_URL)
            return redirect(redirect_to)

    if request.user.is_authenticated:
        # User is already signed in, redirect them to User Home.
        return redirect(reverse_lazy(settings.LOGIN_REDIRECT_URL))

    return render(
        request,
        template_name,
        {
            "next": request.GET.get("next", reverse_lazy(settings.LOGIN_REDIRECT_URL)),
            "login_form": login_form,
            "registration_form": registration_form,
        },
    )
