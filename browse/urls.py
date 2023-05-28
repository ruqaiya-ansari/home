from django.urls import path
from . import views

app_name = 'browse'

urlpatterns = [
    path('like/', views.image_like, name='likes'),
    path('<int:pk>/<slug:slug>/', views.BookDetailView.as_view(), name='books_detail'),
    path('search/pages/', views.search_view, name="search"),
    path('search/pages/<str:text>', views.search_view, name="searches"),
    path('browse/<slug:category_slug>', views.BrowseCategory.as_view(), name='genre'),
    path('Edit/<pk>', views.ReviewEdit.as_view(), name="review_edit"),
    path('homes', views.HomeV.as_view(), name="homes"),

    path('Delete/<pk>', views.ReviewDelete.as_view(), name="review_delete"),
    path('novel/pages/', views.Listing.as_view(), name='listing'),
    path('story/pages/', views.ListingStory.as_view(), name='story'),
    path('browse', views.Browse.as_view(), name="browse"),

]
