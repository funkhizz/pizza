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
from custom_user.forms import EmailUserCreationForm, EmailUserChangeForm

User = get_user_model()


class CustomUserEditForm(EmailUserChangeForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)

    email = forms.EmailField(
        required=True,
        max_length=255,
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field("password", type="hidden"),
            Row(
                Div("first_name", css_class="col-sm-6"),
                Div("last_name", css_class="col-sm-6"),
            ),
            Row(
                Div("email", css_class="col-sm-6"),
            ),
            ButtonHolder(
                Submit("submit", _("Save changes")),
                HTML(
                    "<a href='{0}' class='btn btn-link'>"
                    "{1}</a>".format(
                        reverse_lazy("users:home"),
                        _("Cancel"),
                    )
                ),
            ),
        )

        super(CustomUserEditForm, self).__init__(*args, **kwargs)


class CustomUserCreationForm(EmailUserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)

    email = forms.EmailField(
        label="Email address",
        required=True,
        max_length=255,
        help_text="This is also your username to sign in to your account.",
    )

    email2 = forms.EmailField(
        label=_("Email address confirmation"),
        required=True,
        max_length=255,
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=mark_safe(password_validators_help_text_html()),
    )

    class Meta(EmailUserCreationForm.Meta):
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

    def clean_email(self):
        # Since EmailUser.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data.get("email")
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages["duplicate_email"])

    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email and email2 and email != email2:
            raise forms.ValidationError("Email addresses do not match.")
        return email2

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        usr = User(
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
            email=self.cleaned_data.get("email"),
        )

        validate_password(password1, user=usr)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password2 != password1:
            self.add_error(
                "password2",
                forms.ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                ),
            )
        return password2

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div("first_name", css_class="col-sm-6"),
            Div("last_name", css_class="col-sm-6"),
            "email",
            Field("email2", placeholder="Retype email for verification"),
            "password1",
            Field("password2", placeholder="Retype password for verification"),
        )

        super(CustomUserCreationForm, self).__init__(*args, **kwargs)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.pop("autofocus", None)
