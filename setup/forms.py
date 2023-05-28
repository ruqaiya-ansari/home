from django import forms
from django.forms.models import inlineformset_factory
from .models import Books, Chapter

ChapterFormSet = inlineformset_factory(Books, Chapter, fields=['title'], extra=2, can_delete=True)
