from library.library import BookList
from .models import Books

def myList(request):
    book_list = BookList(request)
    book_ids = book_list.book_list.keys()
    books = Books.objects.filter(id__in=book_ids)
    return {'myList': books}
