from django.urls import path
from . import views

app_name= 'blog'

urlpatterns = [
    path('home/', views.ArticleList.as_view(), name='bloghome'),
path('detail/<slug:slug>', views.ArticleDetail.as_view(), name='article-detail'),


]