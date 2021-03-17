from django.shortcuts import render
from django.views.generic.base import TemplateView

class IndexView (TemplateView):
    template_name: str = "forum/index.html"
