import datetime
import uuid

from django.db import models

# Create your models here.
from apps.user.models import User


class Author(models.Model):
    """
    Modelo que representa un autor
    """
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_birth = models.DateField(null=True, blank=True)
    date_die = models.DateField('Died', null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"


class Book(models.Model):
    """
    Modelo que representa un libro
    """
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=255, null=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.code} {self.title} {self.author} {self.quantity}"


class Loan(models.Model):
    """
    Modelo que representa el detalle de un prestamos
    """
    reader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='prestamista')
    loan_date = models.DateTimeField(auto_now_add=True, null=True)
    book_instance = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='libros')
    state = models.CharField(max_length=50, default="Temporalmente Reservado")

    def __str__(self):
        return f"{self.loan_date}  {self.book_instance.title}"




class Reservacion(models.Model):
    books = models.ManyToManyField(Loan, related_name='prestados')
    date_reservation = models.DateTimeField(auto_now_add=True, null=True)
    date_end = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(30))
    user = models.ForeignKey(User, related_name="lector", on_delete=models.CASCADE, null=True)
