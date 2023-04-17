from django.urls import path

from . import views

api_url_patterns = [
    path("search/", views.search, name="index"),
    path("", views.search, name="index"),
]