from django.db import models
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from .fields import OrderField
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField(upload_to='books/')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Books(models.Model):
    BOOk_CHOICE = (('Text', 'Text'),
                   ('Image', 'Image'))
    BOOK_TYPE = (('NOVEL', 'NOVEL'),
                 ('SHORT-STORY', 'SHORT-STORY'))
    category = models.ManyToManyField(Category, related_name='books')
    title = models.CharField(max_length=200)
    popular = models.BooleanField(default=False)
    genre = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='books/')
    description = models.TextField(blank=False)
    author = models.CharField(max_length=250, blank=False)
    bookType = models.CharField(max_length=250, choices=BOOK_TYPE, default='NOVEL')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    page_type = models.CharField(max_length=250, choices=BOOk_CHOICE, default='Text')
    tags = TaggableManager()
    user_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="books_liked", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('browse:books_detail', kwargs={'pk': self.pk, 'slug': self.slug})


class Quotes(models.Model):
    book = models.ForeignKey(Books, related_name='book_quotes', on_delete=models.CASCADE)
    character = models.CharField(max_length=100)
    quotes = models.TextField()


class Chapter(models.Model):
    book = models.ForeignKey(Books, related_name='chapter', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, blank=False)
    order = OrderField(blank=True, for_fields=['book'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Content(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='content', on_delete=models.CASCADE,
                                limit_choices_to={'model__in': ('Text', 'Image')})

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    page = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['chapter'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    class Meta:
        abstract = True

    def render(self):
        return render_to_string('Books/content/{}.html'.format(self._meta.model_name), {'page': self})


class Text(ItemBase):
    text = models.TextField()


class Image(ItemBase):
    image = models.ImageField(upload_to='book/page')