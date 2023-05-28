from django.conf import settings


class BookList(object):
    def __init__(self, request):
        self.session = request.session
        book_list = self.session.get(settings.BOOK_LIST_ID)
        read_list = self.session.get(settings.READ_LIST_ID)
        if not book_list:
            book_list = self.session[settings.BOOK_LIST_ID] = {}
        if not read_list:
            read_list = self.session[settings.READ_LIST_ID] = {}
        self.book_list = book_list
        self.read_list = read_list

    def add(self, book):
        book_id = str(book.id)
        if book_id not in self.book_list:
            self.book_list[book_id] = {'book_title': str(book.title)}
        self.save()

    def read_add(self, chapter, update_chapter=False):
        chapter_id = str(chapter.id)
        book_id = str(chapter.book.id)

        if book_id not in self.read_list:
            self.read_list[book_id] = {'chapter_id': chapter_id}

        if update_chapter:
            self.read_list[book_id]['chapter_id'] = chapter_id

        self.save()

    def read_remove(self, book):
        book_id = str(book.id)
        if book_id in self.read_list:
            del self.read_list[book_id]
            self.save()

    def save(self):
        self.session.modified = True

    def remove(self, book):
        book_id = str(book.id)
        if book_id in self.book_list:
            del self.book_list[book_id]
            self.save()

    def clear(self):
        del self.book_list[settings.BOOK_LIST_ID]
        self.save()
