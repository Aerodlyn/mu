from django.urls import path

from .views import (
    CommunityListView,
    IndexView
)

urlpatterns = [
    path ("", IndexView.as_view (), name = "index"),
    path ("communities", CommunityListView.as_view (), name = "community-list")
]
