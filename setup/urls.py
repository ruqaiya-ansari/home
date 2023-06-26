from django.urls import path
from . import views
from .feeds import LatestBookFeeds

app_name = 'setup'
urlpatterns = [
    path('mine/', views.ManageBooksListView.as_view(), name='update_books'),
    path('create/', views.BookCreateView.as_view(), name='book_create'),
    path('<pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('<pk>/delete', views.BookDeleteView.as_view(), name='book_delete'),
    path('feed/', LatestBookFeeds(), name='book_feed'),
    path('searches/', views.search, name="searches"),
    path('<pk>/chapter/', views.ChapterUpdateView.as_view(), name='edit_chapters'),
    path('chapter/<int:chapter_id>/content/create/', views.ContentCreateUpdateView.as_view(),
         name='chapter_content_create'),
    path('chapter/<int:chapter_id>/content/<id>/', views.ContentCreateUpdateView.as_view(),
         name='chapter_content_update'),
    path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='chapter_content_delete'),
    path('chapter/order/', views.ChapterOrderView.as_view(), name='chapter_order'),
    path('content/order/', views.ContentOrderView.as_view(), name='page_order'),
    path('chapter/<int:chapter_id>/', views.ChapterContentListView.as_view(), name='chapter_content_list'),
]
