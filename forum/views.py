from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.contrib.auth.models import Group
from django.db.models.functions import Lower
from django.forms import BaseForm
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect
)
from django.shortcuts import get_object_or_404
from django.urls import (
    reverse,
    reverse_lazy
)
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView
)
from django.views.generic.list import (
    ListView,
    MultipleObjectMixin
)

from .forms import (
    CommunityCreateForm,
    CommunityUpdateForm,
    PostCreateForm
)
from .models import (
    Community,
    Post
)

# Community-related views
class CommunityCreateView (LoginRequiredMixin, CreateView):
    template_name       : str                   = "forum/community/community-create.html"
    form_class          : CommunityCreateForm   = CommunityCreateForm

    # Override
    def form_valid (self, form: BaseForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super ().form_valid (form)

class CommunityDeleteView (PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    success_url     : str       = reverse_lazy ("forum:index")
    template_name   : str       = "forum/community/community-delete.html"
    model           : Community = Community

    # Override
    def has_permission (self) -> bool:
        return self.get_object ().is_user_moderator (self.request.user)
    
class CommunityDetailView (PermissionRequiredMixin, DetailView, MultipleObjectMixin):
    paginate_by     : int       = 10
    template_name   : str       = "forum/community/community-detail.html"
    model           : Community = Community    

    # Override
    def has_permission (self) -> bool:
        return not self.get_object ().private or self.is_request_user_member ()

    # Override
    def get_context_data (self, **kwargs: dict) -> dict:
        posts = self.get_object ().post_set.order_by ("-created_at").all ()
        return super ().get_context_data (object_list = posts, **kwargs)

    def is_request_user_member (self) -> bool:
        """See Community.is_user_member"""
        return self.get_object ().is_user_member (self.request.user)

    def is_request_user_moderator (self) -> bool:
        """See Community.is_user_moderator"""
        return self.get_object ().is_user_moderator (self.request.user)

class CommunityListView (ListView):
    paginate_by     : int       = 10
    ordering        : list      = [ Lower ("name") ]
    template_name   : str       = "forum/community/community-list.html"

    model           : Community = Community

class CommunitySubscribedListView (LoginRequiredMixin, CommunityListView):
    # Override
    def get_queryset (self):
        return Community.objects.filter (members = self.request.user).order_by (Lower ("name"))

class CommunityUpdateView (PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name       : str                   = "forum/community/community-update.html"
    model               : Community             = Community
    form_class          : CommunityUpdateForm   = CommunityUpdateForm

    # Override
    def has_permission (self) -> bool:
        return self.get_object ().is_user_moderator (self.request.user)

@login_required
@require_POST
def update_user_community_membership (request: HttpRequest, slug: str) -> HttpResponse:
    community: Community = get_object_or_404 (Community, slug = slug)
    if community.is_user_member (request.user):
        community.remove_user (request.user)
    else:
        community.add_user (request.user)

    return HttpResponseRedirect (reverse ("forum:community-detail", kwargs = { "slug": slug }))

# Post-related views
class PostCreateView (PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name       : str               = "forum/post/post-create.html"
    form_class          : PostCreateForm    = PostCreateForm

    @property
    def community (self) -> Community:
        try:
            self._community
        except AttributeError:
            self._community = Community.objects.get (slug = self.kwargs ["community_slug"])
        return self._community
    
    # Override
    def form_valid (self, form: BaseForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        form.instance.posted_in = self.community

        return super ().form_valid (form)

    # Override
    def has_permission (self) -> bool:
        return not self.community.private or self.community.is_user_member (self.request.user)

class PostDetailView (PermissionRequiredMixin, DetailView):
    template_name   : str   = "forum/post/post-detail.html"
    model           : Post  = Post

    # Override
    def has_permission (self) -> bool:
        community: Community = self.get_object ().posted_in
        return not community.private or community.is_user_member (self.request.user)

# Etc. views
class IndexView (TemplateView):
    template_name: str = "forum/index.html"
