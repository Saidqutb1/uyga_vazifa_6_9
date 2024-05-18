from django.forms import ModelForm
from django import forms
from .models import Review, Books

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'description', 'price', 'category', 'page', 'image', 'book_lang']


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['star_given']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['star_given']