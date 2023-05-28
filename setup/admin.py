from django.contrib import admin
from .models import Category, Books, Chapter,Quotes


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ChapterInline(admin.StackedInline):
    model = Chapter

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'description', 'image', 'page_type', 'popular']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['title', 'author']
    search_fields = ['title', 'author']
    inlines = [ChapterInline]

@admin.register(Quotes)
class BookQuotes(admin.ModelAdmin):
    list_display = ['book', 'character', 'quotes']


