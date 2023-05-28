from django.urls import path
from . import views

app_name='library'

urlpatterns = [
    path('view/', views.Library.as_view(), name='list_detail'),

    path('add/<int:book_id>/',
         views.book_add,
         name='book_add'),

    path('continue-remove/<int:book_id>/', views.read_delete, name='read_remove'),

    path('remove/', views.book_delete, name='lib_remove'),

]
