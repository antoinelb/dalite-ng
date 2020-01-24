from django.urls import path

from . import views

app_name = "courseflow"
urlpatterns = [
    path("", views.index, name="index",),
]
