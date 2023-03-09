from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.search_view),
    path("wiki/<str:entry_title>", views.entry, name="entry"),
    path("add/", views.add, name="add"),
    path("edit/<str:entry_title>", views.edit, name="edit"),
    path("random", views.random, name="random")
    
]
