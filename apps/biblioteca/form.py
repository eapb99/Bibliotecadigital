from django import forms

from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['code', "title", "quantity", "author"]
