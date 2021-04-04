from django.urls import path
from django.views.generic.edit import CreateView

from .views import (
    CommunityCreateView,
    CommunityDetailView,
    CommunityListView,
    IndexView,
    update_user_community_membership
)

urlpatterns = [
    path ("", IndexView.as_view (), name = "index"),

    # Communities Views
    path ("communities", CommunityListView.as_view (), name = "community-list"),
    path ("communities/new", CommunityCreateView.as_view (), name = "community-create"),
    path ("communities/<slug:slug>", CommunityDetailView.as_view (), name = "community-detail"),
    path ("communities/<slug:slug>/update-membership", update_user_community_membership, name = "community-update-membership")
]
