from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.contrib.auth.models import Group
from django.db.models.functions import Lower
from django.forms import BaseForm
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import CommunityCreateForm
from .models import Community

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

class IndexView (TemplateView):
    template_name: str = "forum/index.html"
