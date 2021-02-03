from django.urls import path
from .views import HomeView, login_or_register, RegistrationView

app_name = "users"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login-register/", login_or_register, name="login-or-register"),
    path("register/", RegistrationView.as_view(), name="register")
]
