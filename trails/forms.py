from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    # Define choices for rating
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent')
    ]

    # Override the comment field
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'required': True
    }))

    # Override the rating field
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control',
        'required': True
    }))

    class Meta:
        model = Review
        fields = ['comment', 'rating']