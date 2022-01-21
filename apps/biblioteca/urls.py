from django.urls import path
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register('book', BookViewSet)
router.register('author', AuthorViewSet)
router.register('loan', LoanViewSet)
urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('detail/<str:pk>', DetailBook.as_view(), name='detail'),
    path('eliminar/<int:producto_id>/', eliminar_producto, name="Del"),
    path('reservas/', reservas, name="reservas"),
    path('list/', ListReservaciones.as_view(), name="list-reservas"),
]

urlpatterns += router.urls
