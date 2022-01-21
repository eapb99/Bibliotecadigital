# Create your views here.
import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from rest_framework.response import Response

from apps.biblioteca.models import Book, Author, Loan, Reservacion
from apps.biblioteca.util.serializers import BookSerializer, AuthorSerializer, LoanSerializer
from .form import BookForm
from .util.util import Carrito
from ..user.models import User


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        code = data['code']
        objeto = Book.objects.filter(code=code)
        serializer = ""
        if len(objeto) > 0:
            objeto[0].quantity += 1
            objeto[0].save()
            serializer = BookSerializer(objeto[0])
        else:
            new_book = Book.objects.create(code=data['code'], title=data['title'], author=data['author'],
                                           quantity=data['quantity'])
            new_book.save()
            serializer = BookSerializer(new_book)
        return Response(serializer.data)


"""
    def update(self, request, *args, **kwargs):
        print(request.data)"""


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        book = Book.objects.get(id=data['book_instance'])
        query = User.objects.get(pk=request.user.pk).prestamista.all().filter(book_instance_id=book.id).exclude(
            state="Cancelado").exclude(state="Devuelto")
        query2 = Loan.objects.filter(book_instance_id=data['book_instance']).filter(state="Temporalmente Reservado")
        cantidad1 = query2.count()
        cantidad = query.count()
        if cantidad > 0:
            return Response({'data': 'Ya tiene prestado o tiene temporalmente reservado un libro con este código'})
        elif cantidad1 > 0:
            return Response({'data': 'Este libro se encuentra temporalmente reservado,intentelo mas tarde'})
        else:
            new_loan = Loan.objects.create(book_instance_id=data['book_instance'], reader_id=data['reader'])
            new_loan.save()
            serializer = LoanSerializer(new_loan)
            return Response(serializer.data)


class DashboardView(ListView):
    template_name = 'index.html'
    model = Book
    paginate_by = 10

    def get_queryset(self):
        books = Book.objects.all()
        return books

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Principal Page"
        context['title_object'] = "Listado de Libros"
        context['prestamos'] = User.objects.get(pk=self.request.user.pk).prestamista.all().filter(
            state="Temporalmente Reservado")
        context['form'] = BookForm()
        context['list_url'] = reverse_lazy('index')
        return context


class DetailBook(DetailView):
    template_name = 'detail.html'
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Detalle de Libro"
        context['fetch'] = reverse_lazy('loan-list')
        return context


class ListReservaciones(ListView):
    model = Reservacion
    template_name = "estudiante/lista_reservados.html"

    def get_queryset(self):
        qs = self.model.objects.filter(user_id=self.request.user.pk)
        return qs


def eliminar_producto(request, producto_id):
    user = User.objects.get(pk=request.user.pk)
    prestamo = Loan.objects.get(id=producto_id)
    user.prestamista.remove(prestamo)
    prestamo.state = "Cancelado"
    prestamo.save()
    return redirect("index")


def reservas(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        reservas = Reservacion.objects.create(user_id=request.user.pk)
        for id in body['id']:
            prestamo = Loan.objects.get(pk=id)
            prestamo.state = "Prestado"
            prestamo.save()
            libro = Book.objects.get(pk=prestamo.book_instance.pk)
            libro.quantity -= 1
            libro.save()
            reservas.books.add(prestamo)
        reservas.save()
        return JsonResponse({"data": "Reserva realizada exitosamente"})
