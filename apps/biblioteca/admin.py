from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'quantity', 'id']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ["loan_date", "book_instance", "reader", "state"]


@admin.register(Reservacion)
class ReservacionAdmin(admin.ModelAdmin):
    list_display = ['date_reservation', "date_end", "user"]
