from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomeView, login_or_register, RegistrationView, UpdateAccountView

app_name = "users"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login-register/", login_or_register, name="login-or-register"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView),

    # Account management stuff
    path("my-details/", UpdateAccountView.as_view(), name="details"),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView,
        {"template_name": "pages/users/update_password_done.html"},
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView,
        {"template_name": "pages/users/update_password.html"},
    ),
]
