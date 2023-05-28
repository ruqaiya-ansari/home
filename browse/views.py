from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from django.views.generic.list import ListView
from .models import Review
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import UpdateView, DeleteView
from setup.models import Books, Category, Chapter
from library.library import BookList
from django.db.models import Q
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from .forms import ReviewForm
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError


class HomeV(View, TemplateResponseMixin):
    template_name = 'myview.html'

    def get(self, request, *args, **kwargs):
        library = BookList(request)
        reading_ids = library.read_list.keys()

        chapters_id = [library.read_list[str(book)]['chapter_id'] for book in reading_ids]

        chapter_books = Chapter.objects.filter(id__in=chapters_id)

        new_arrivals = Books.objects.order_by('-publish')[:5]

        # Get that object:

        books_by_popularity = Books.objects.filter(popular=True)
        Featured = Books.objects.filter(Q(genre="action"))[:5]
        our_suggestion = Books.objects.all()[:5]
        stories = Books.objects.filter(bookType="SHORT-STORY")[:5]

        return self.render_to_response({'reading': chapter_books, 'arrival': new_arrivals,
                                         'popular': books_by_popularity, 'featured': Featured, 'suggest':
                                            our_suggestion, "story":stories},
                                       )


class BookDetailView(TemplateResponseMixin, View):
    obj = None
    template_name = 'BookDetail.html'


    def dispatch(self, request, pk, slug):
        self.obj = get_object_or_404(Books,
                                     id=pk,
                                     slug=slug)

        return super(BookDetailView, self).dispatch(request, pk, slug)

    def final_rating(self):
        ratings = Review.objects.filter(book=self.obj)
        num_ratings = ratings.count()
        if num_ratings > 0:
            avg_rating = sum(r.rating for r in ratings) / num_ratings

            return (num_ratings / (num_ratings + 5)) * avg_rating + (5 / (num_ratings + 5)) * 3

    def get(self, *args, **kwargs):
        form = ReviewForm()
        weighted_rating = self.final_rating()
        this_genre = self.obj.genre
        related_books = Books.objects.filter(Q(genre=this_genre)).exclude(id=self.obj.id)

        return self.render_to_response({'review_form': form, 'object': self.obj, "related_books": related_books,
                                        'book_rating': weighted_rating
                                        })

    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        form = ReviewForm(self.request.POST)
        weighted_rating = self.final_rating()
        related_books = Books.objects.all()

        try:

            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.book = self.obj
                new_review.user = self.request.user
                new_review.save()

        except IntegrityError:
            return HttpResponse("You have already review")

        return self.render_to_response({'review_form': form, 'object': self.obj, "related_books": related_books,
                                        'book_rating': weighted_rating})


class Browse(View, TemplateResponseMixin):
    template_name = 'browse.html'

    def get(self, request):
        category = Category.objects.all()
        mystery_books = Books.objects.filter(Q(genre="mystery") | Q(genre="fantasy"))[:5]
        action_books = Books.objects.filter(Q(genre="action"))[:5]
        romance = Books.objects.filter(Q(genre="romance"))[:5]

        return self.render_to_response(
            {'category': category, 'mystery_books': mystery_books, 'action_books': action_books, 'romance': romance})


class Listing(ListView):
    # specify the model for list view
    model = Books
    template_name = 'collection.html'

    def get_queryset(self, *args, **kwargs):
        return super(Listing, self).get_queryset(*args, **kwargs).filter(bookType="NOVEL")


class ListingStory(ListView):
    # specify the model for list view
    model = Books
    template_name = 'story.html'
    context_object_name = 'story'

    def get_queryset(self, *args, **kwargs):
        return super(ListingStory, self).get_queryset(*args, **kwargs).filter(bookType="SHORT-STORY")


class BrowseCategory(View, TemplateResponseMixin):
    template_name = 'BookCategory.html'

    def get(self, request, category_slug):
        books = Category.objects.get(slug=category_slug)
        return self.render_to_response({'books': books})


class ReviewEdit(UpdateView):
    model = Review
    fields = ['rating', 'body']
    template_name = 'ReviewEdit.html'

    def get_success_url(self):
        return reverse_lazy('browse:books_detail',
                            kwargs={'pk': self.get_object().book.id, 'slug': self.get_object().book.slug})


class ReviewDelete(DeleteView):
    model = Review

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('browse:books_detail',
                            kwargs={'pk': self.get_object().book.id, 'slug': self.get_object().book.slug})


@require_POST
@login_required
def image_like(request):
    id = request.POST.get('id')
    action = request.POST.get('action')
    if action and id:
        try:
            book = Books.objects.get(id=id)
            if action == 'like':

                book.user_likes.add(request.user)
            else:
                book.user_likes.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass

    return JsonResponse({'status': 'ko'})


def search_view(request):
    results = None
    cate = Books.objects.all()[:5]
    search_text = request.GET.get('search_text')

    if search_text:

        results = Books.objects.filter(title__icontains=search_text)

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            html = render_to_string(
                template_name="search_ajax.html",
                context={"results": results}
            )

            data_dict = {"html_from_view": html}

            return JsonResponse(data=data_dict, safe=False)

    return render(request, "search.html", {'cate': cate, 'results': results})

