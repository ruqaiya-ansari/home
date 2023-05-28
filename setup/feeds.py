from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Books

class LatestBookFeeds(Feed):
    title ="clasicReads"
    link = '/books/'

    def items(self):
        return Books.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.description, 30)