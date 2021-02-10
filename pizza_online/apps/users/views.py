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

from .tasks import send_welcome_email
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


class RegistrationView(BaseRegistrationView):
    form_class = CustomUserCreationForm
    template_name = "registration/login_or_register.html"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)

        context.update(
            {
                "next": self.request.GET.get(
                    "next", reverse_lazy(settings.LOGIN_REDIRECT_URL)
                ),
                "login_form": LoginForm(),
                "registration_form": CustomUserCreationForm(),
            }
        )
        return context

    def register(self, form):
        user_model = get_user_model()
        user_model._default_manager.create_user(
            form.cleaned_data["email"],
            form.cleaned_data["password1"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            is_active=True,
        )

        new_user = authenticate(
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
        )

        auth_login(self.request, new_user)
        send_welcome_email(new_user.get_short_name(), new_user.email, self.request)
        return new_user

    def get_success_url(self, user):
        return self.request.POST.get("next", reverse_lazy(settings.LOGIN_REDIRECT_URL))

    def form_invalid(self, form):
        context = self.get_context_data()
        context["registration_form"] = form
        return render(self.request, self.template_name, context)


class UpdateAccountView(ProtectedView, UpdateView):
    """
    Manage personal account details
    """

    form_class = CustomUserEditForm
    template_name = "pages/users/update_account.html"
    success_url = ""

    def get_object(self, queryset=None):
        obj = get_object_or_404(User, id=self.request.user.pk)
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        messages.success(self.request, _("Your details have been updated."))
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.GET.get("next", reverse("users:details"))

