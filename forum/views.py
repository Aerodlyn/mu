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
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import CommunityCreateForm
from .models import Community

# Community-related views
class CommunityCreateView (LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required : str                   = "forum.add_community"
    template_name       : str                   = "forum/community/community-create.html"
    form_class          : CommunityCreateForm   = CommunityCreateForm

    # Override
    def form_valid (self, form: BaseForm) -> HttpResponse:
        form.instance.created_by = self.request.user
        return super ().form_valid (form)
    
class CommunityDetailView (PermissionRequiredMixin, DetailView):
    template_name   : str       = "forum/community/community-detail.html"
    model           : Community = Community    

    # Override
    def has_permission (self) -> bool:
        return not self.get_object ().private or self.is_request_user_member ()

    def is_request_user_member (self) -> bool:
        """See Community.is_user_member"""
        return self.get_object ().is_user_member (self.request.user)

class CommunityListView (ListView):
    paginate_by     : int       = 10
    ordering        : list      = [ Lower ("name") ]
    template_name   : str       = "forum/community/community-list.html"

    model           : Community = Community

@login_required
@require_POST
def update_user_community_membership (request: HttpRequest, slug: str) -> HttpResponse:
    community: Community = get_object_or_404 (Community, slug = slug)
    if community.is_user_member (request.user):
        community.remove_user (request.user)
    else:
        community.add_user (request.user)

    return HttpResponseRedirect (reverse ("community-detail", kwargs = { "slug": slug }))

# Etc. views
class IndexView (TemplateView):
    template_name: str = "forum/index.html"
