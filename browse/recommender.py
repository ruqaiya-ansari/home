import redis
from setup.models import Books
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommender(object):

    def get_book_key(self, id):
        return 'book:{}read_with'.format(id)

    def book_read(self, books):
        book_ids = [b.id for b in books]
        for book_id in book_ids:
            for with_id in book_ids:
                if book_id != with_id:
                    r.zincrby(self.get_book_key(book_id), with_id, amount=1)

    def get_suggested_books(self, books, max_results=6):
        book_id = [b.id for b in books]
        if len(books) == 1:
            suggested_books = r.zrange(self.get_book_key(book_id[0]), 0, -1, desc=True)[:max_results]
        else:
            flat_ids = ''.join([str(id) for id in book_id])
            tmp_key = 'tmp_{}'.format(flat_ids)
            keys = [self.get_book_key(id) for id in book_id]
            r.zunionstore(tmp_key, keys)
            r.zrem(tmp_key, *book_id)
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            suggested_books_ids = [int(id) for id in suggestions]
            suggested_books = list(Books.objects.filter(id__in=suggested_books_ids))
            suggested_books.sort(key=lambda x: suggested_books_ids.index(x.id))
        return suggested_books
