from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView

from .models import Profile

class ProfileDetailView (DetailView):
    template_name   : str       = "user/profile/profile-view.html"
    model           : Profile   = Profile

    # Override
    def get_object (self, queryset: QuerySet = None) -> Profile:
        if queryset is None:
            queryset = self.get_queryset ()

        return get_object_or_404 (queryset, user__username = self.kwargs ["username"])
