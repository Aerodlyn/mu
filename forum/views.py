from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import CommunityCreateForm
from .models import Community

class CommunityCreateView (LoginRequiredMixin, CreateView):
    template_name   : str                   = "forum/community/community-create.html"
    form_class      : CommunityCreateForm   = CommunityCreateForm

class CommunityListView (ListView):
    paginate_by     : int       = 10
    ordering        : list      = [ Lower ("name") ]
    template_name   : str       = "forum/community/community-list.html"

    model           : Community = Community

class IndexView (TemplateView):
    template_name: str = "forum/index.html"
