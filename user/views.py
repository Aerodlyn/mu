from django.contrib.auth.mixins import LoginRequiredMixin
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

from .forms import ProfileUpdateForm
from .models import Profile

class ProfileDetailView (DetailView):
    template_name   : str       = "user/profile/profile-view.html"
    model           : Profile   = Profile

    # Override
    def get_object (self, queryset: QuerySet = None) -> Profile:
        if queryset is None:
            queryset = self.get_queryset ()

        return get_object_or_404 (queryset, user__username = self.kwargs ["username"])

class ProfileUpdateView (LoginRequiredMixin, UpdateView):
    template_name   : str               = "user/profile/profile-update.html"

    form_class      : ProfileUpdateForm = ProfileUpdateForm
    model           : Profile           = Profile

    # Override
    def get (self, request: HttpRequest, *args: tuple, **kwargs: list) -> HttpResponse:
        if request.user.is_authenticated and kwargs ["username"] != request.user.username:
            return HttpResponseRedirect (reverse_lazy ("profile-update", kwargs = { "username": request.user.username }))
        return super ().get (request, *args, **kwargs)

    def get_object (self, queryset: QuerySet = None) -> Profile:
        if queryset is None:
            queryset = self.get_queryset ()

        return get_object_or_404 (queryset, user = self.request.user)
