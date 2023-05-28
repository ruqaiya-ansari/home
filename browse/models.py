from django.db import models
from setup.models import Books

from django.conf import settings


# Create your models here.
class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_review')
    body = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-created',]

    def __str__(self):
        return 'Review by {} on {}'.format(self.user, self.book)


