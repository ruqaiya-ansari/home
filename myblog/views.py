
from django.views.generic.list import ListView
from .models import Article
from django.views.generic.detail import DetailView




class ArticleList(ListView):
    model = Article
    template_name = 'blog-list.html'


class ArticleDetail(DetailView):
    model = Article
    template_name = 'blog-detail.html'