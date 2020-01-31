from django.urls import path

from . import views

app_name = "courseflow"
urlpatterns = [
    path("login", views.login, name="login"),
    path("authenticate", views.authenticate, name="authenticate"),
    path("courseflow", views.courseflow, name="courseflow"),
]
