from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from .models import Community

class CommunityListView (ListView):
    paginate_by     : int       = 10
    ordering        : list      = [ "name" ]
    template_name   : str       = "forum/community/community-list.html"

    model           : Community = Community

class IndexView (TemplateView):
    template_name: str = "forum/index.html"
