from django.urls import path, re_path

from . import views
from django.conf.urls import url

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.title, name='title'),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("wiki/edit/<str:name>", views.edit, name="edit"),
    path("randompg", views.randompg, name="randompg")
]
