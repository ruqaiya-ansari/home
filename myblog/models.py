from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField


# Create your models here.
class Article(models.Model):
    STATUS_CHOICE = (('draft', 'Draft'),
                     ('published', 'Published'))
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.CharField(max_length=250)
    image = models.ImageField(upload_to='blog/')
    body = RichTextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

