
from django.http import JsonResponse
from django.shortcuts import  redirect, get_object_or_404

from setup.models import Books
from django.views.generic.list import ListView
from .library import BookList


# Create your views here.

def book_add(request, book_id):
    book_list = BookList(request)
    book = get_object_or_404(Books, id=book_id)
    book_list.add(book)
    return redirect('library:list_detail')


def read_delete(request, book_id):
    book_list = BookList(request)
    book = get_object_or_404(Books, id=book_id)
    book_list.read_remove(book)
    return redirect('setup:homes')


def book_delete(request):
    book_list = BookList(request)
    book_id = request.GET.get('id')
    book = get_object_or_404(Books, id=book_id)
    book_list.remove(book)
    return JsonResponse({'status': 'ok'})


class Library(ListView):
    template_name = 'lib.html'
    model = Books

    def get_queryset(self):
        book_obj = BookList(self.request)
        book_id = book_obj.book_list.keys()

        return super(Library, self).get_queryset().filter(id__in=book_id)
# Create your views here.
