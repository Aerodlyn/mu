from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from extra_views import UpdateWithInlinesView

from .forms import (
    ProfileInlineFormSet,
    UserUpdateForm
)
from .models import Profile

class ProfileDetailView (DetailView):
    template_name   : str       = "user/profile/profile-detail.html"
    model           : Profile   = Profile

    # Override
    def get_object (self, queryset: QuerySet = None) -> Profile:
        if queryset is None:
            queryset = self.get_queryset ()

        return get_object_or_404 (queryset, user__username = self.kwargs ["username"])

class ProfileUpdateView (LoginRequiredMixin, UpdateWithInlinesView):
    inlines         : list              = [ ProfileInlineFormSet ]
    template_name   : str               = "user/profile/profile-update.html"

    form_class      : UserUpdateForm    = UserUpdateForm
    model           : User              = User

    # Override
    def get_success_url (self, *args: list, **kwargs: dict) -> str:
        return reverse_lazy (
            "user:profile-detail",
            kwargs = { "username": self.request.user.username }
        )

    # Override
    def get (self, request: HttpRequest, *args: list, **kwargs: dict) -> HttpResponse:
        if request.user.is_authenticated and kwargs ["username"] != request.user.username:
            return HttpResponseRedirect (self.get_success_url ())
        return super ().get (request, *args, **kwargs)

    # Override
    def get_object (self, queryset: QuerySet = None) -> User:
        if queryset is None:
            queryset = self.get_queryset ()

        return queryset.get (pk = self.request.user.pk)
