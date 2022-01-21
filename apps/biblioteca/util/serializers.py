from apps.biblioteca.models import Book, Author, Loan
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'last_name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'code', 'title', 'quantity', 'author']


class LoanSerializer(serializers.ModelSerializer):
    book_instance = BookSerializer()

    class Meta:
        model = Loan
        fields = ['id', 'state', "book_instance", 'reader', 'loan_date']
