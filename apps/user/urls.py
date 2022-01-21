from django.urls import path

from .views import *

urlpatterns = [
    path("", LoginFormView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
]