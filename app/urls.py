from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_url", views.add_url, name="add_url"),
]
