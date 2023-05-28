from .models import Review
from django import forms


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body', 'rating')

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.TextInput(
            attrs={'class': 'forms',  'id': 'review_form'})
        self.fields['body'].label = False
