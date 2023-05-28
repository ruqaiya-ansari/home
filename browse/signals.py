from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from setup.models import Books


@receiver(m2m_changed, sender=Books.user_likes.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.user_likes.count()
    instance.save()
