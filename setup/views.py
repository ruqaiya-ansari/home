from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.forms.models import modelform_factory
from django.apps import apps
from .models import Books, Chapter, Content
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from library.library import BookList
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin, SuperuserRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import ChapterFormSet
from django.views.generic.base import TemplateResponseMixin, View


# Create your views here.
class BookEditMixin(object):
    model = Books
    fields = ['category', 'title', 'image', 'description', 'slug', 'author', 'page_type']

    success_url = reverse_lazy('setup:update_books')
    template_name = 'Books/manage/Book/form.html'


class ManageBooksListView(SuperuserRequiredMixin, BookEditMixin, ListView):
    template_name = 'Books/manage/Book/list.html'


class BookCreateView(SuperuserRequiredMixin, BookEditMixin, CreateView):
    pass


class BookUpdateView(SuperuserRequiredMixin, BookEditMixin, UpdateView):
    pass


class BookDeleteView(SuperuserRequiredMixin, BookEditMixin, DeleteView):
    template_name = 'Books/manage/Book/delete.html'


class ChapterUpdateView(SuperuserRequiredMixin, TemplateResponseMixin, View):
    template_name = 'Books/manage/chapter/formset.html'
    book = None

    def get_formset(self, data=None):
        return ChapterFormSet(instance=self.book, data=data)

    def dispatch(self, request, pk):
        self.book = get_object_or_404(Books, id=pk)

        return super(ChapterUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'book': self.book, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('setup:update_books')
        return self.render_to_response({'book': self.book, 'formset': formset})


class ContentCreateUpdateView(SuperuserRequiredMixin, TemplateResponseMixin, View):
    chapter = None
    model = None
    obj = None

    template_name = 'Books/manage/content/form.html'

    def get_model(self):

        model_name = self.chapter.book.page_type

        return apps.get_model(app_label='setup', model_name=model_name)

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=[''])
        return Form(*args, **kwargs)

    def dispatch(self, request, chapter_id, id=None):
        self.chapter = get_object_or_404(Chapter, id=chapter_id)
        self.model = self.get_model()

        if id:
            self.obj = get_object_or_404(self.model, id=id)
        return super(ContentCreateUpdateView, self).dispatch(request, chapter_id, id)

    def get(self, request, chapter_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)

        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, chapter_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=True)

            if not id:
                Content.objects.create(chapter=self.chapter, page=obj)
            return redirect('setup:chapter_content_list', self.chapter.id)

        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(SuperuserRequiredMixin, View):

    def post(self, request, id):
        content = get_object_or_404(Content, id=id)
        chapter = content.chapter
        content.page.delete()
        content.delete()
        return redirect('setup:chapter_content_list', chapter.id)


class ChapterContentListView(TemplateResponseMixin, View):
    template_name = 'Books/manage/chapter/content_list.html'

    def get(self, request, chapter_id):
        chapter = get_object_or_404(Chapter, id=chapter_id)

        book_list = BookList(request)
        if str(chapter.book.id) in book_list.read_list:
            book_list.read_add(chapter, update_chapter=True)
        else:
            book_list.read_add(chapter, update_chapter=False)

        content = Content.objects.filter(chapter=chapter)
        paginator = Paginator(content, 3)
        page = request.GET.get('page')
        try:
            content = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            content = paginator.page(1)
        except EmptyPage:
            if request.is_ajax:
                # If the request is AJAX and the page is out of range
                # return an empty page
                return HttpResponse('')
            # If page is out of range deliver last page of results
            content = paginator.page(paginator.num_pages)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request,
                          'Books/manage/chapter/content_ajax.html',
                          {"chapter": chapter, 'cont': content})

        return self.render_to_response({'chapter': chapter, 'cont': content})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, SuperuserRequiredMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id).update(order=order)

        return self.render_json_response({'status': 'ok'})


class ChapterOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Chapter.objects.filter(id=id).update(order=order)

        return self.render_json_response({'saved': 'ok'})


def search(request):
    search_text = request.GET.get('search_text')

    if search_text:

        results = Books.objects.filter(title__icontains=search_text)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            html = render_to_string(
                template_name="Books/manage/Book/ajax_search.html",
                context={"results": results}
            )

            data_dict = {"html_from_view": html}
