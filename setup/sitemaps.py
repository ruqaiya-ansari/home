from django.contrib.sitemaps import Sitemap
from .models import Books

class BookSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Books.objects.all()

    def lastmod(self, obj):
        return obj.publish