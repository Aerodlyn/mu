from django.urls import path
from django.views.generic.edit import CreateView

from .views import (
    CommunityCreateView,
    CommunityDeleteView,
    CommunityDetailView,
    CommunityListView,
    CommunitySubscribedListView,
    CommunityUpdateView,
    IndexView,
    PostCreateView,
    PostDetailView,
    update_user_community_membership
)

urlpatterns = [
    path ("", IndexView.as_view (), name = "index"),

    # Communities Views
    path ("communities/all", CommunityListView.as_view (), name = "community-list-all"),
    path ("communities/new", CommunityCreateView.as_view (), name = "community-create"),
    path (
        "communities/subscribed",
        CommunitySubscribedListView.as_view (),
        name = "community-list-subscribed"
    ),
    path ("communities/<slug:slug>", CommunityDetailView.as_view (), name = "community-detail"),
    path (
        "communities/<slug:slug>/delete",
        CommunityDeleteView.as_view (),
        name = "community-delete"
    ),
    path (
        "communities/<slug:slug>/update",
        CommunityUpdateView.as_view (),
        name = "community-update"
    ),
    path (
        "communities/<slug:slug>/update-membership",
        update_user_community_membership,
        name = "community-update-membership"
    ),

    # Post Views
    path (
        "communities/<slug:community_slug>/posts/create",
        PostCreateView.as_view (),
        name = "post-create"
    ),
    path (
        "communities/<slug:community_slug>/posts/<int:id>/<slug:slug>",
        PostDetailView.as_view (),
        name = "post-detail"
    )
]
