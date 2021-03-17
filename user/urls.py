from django.contrib.auth.views import LoginView
from django.urls import (
    path,
    reverse_lazy
)
from django.views.generic.edit import CreateView

from .forms import (
    MuAuthenticationForm,
    MuUserCreationForm
)

urlpatterns = [
    path (
        "login",
        LoginView.as_view (
            authentication_form = MuAuthenticationForm,
            template_name = "user/login/login.html"
        ),
        name = "user-login"
    ),
    path (
        "signup",
        CreateView.as_view (
            form_class = MuUserCreationForm,
            template_name = "user/signup/signup.html",
            success_url = reverse_lazy ("user-login")
        ),
        name = "user-signup"
    )
]
