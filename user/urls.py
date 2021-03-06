from django.contrib.auth.views import (
    LoginView,
    LogoutView
)
from django.urls import (
    path,
    reverse_lazy
)
from django.views.generic.edit import CreateView

from .forms import (
    MuAuthenticationForm,
    MuUserCreationForm
)
from .views import (
    ProfileDetailView,
    ProfileUpdateView
)

urlpatterns = [
    # User access views
    path (
        "login",
        LoginView.as_view (
            authentication_form = MuAuthenticationForm,
            template_name = "user/login/login.html"
        ),
        name = "login"
    ),
    path (
        "logout",
        LogoutView.as_view (),
        name = "logout"
    ),
    path (
        "signup",
        CreateView.as_view (
            form_class = MuUserCreationForm,
            template_name = "user/signup/signup.html",
            success_url = reverse_lazy ("user:login")
        ),
        name = "signup"
    ),
    
    # Profile views
    path (
        "<str:username>",
        ProfileDetailView.as_view (),
        name = "profile-detail"
    ),
    path (
        "<str:username>/edit",
        ProfileUpdateView.as_view (),
        name = "profile-update"
    )
]
