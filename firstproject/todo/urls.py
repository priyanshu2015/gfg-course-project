from django.urls import path
from .views import register, login, logout, list_create_task

urlpatterns = [
    path("signup/", register),
    path("login/", login),
    path("logout/", logout),
    # POST => Create, GET => List Tasks
    path("tasks/", list_create_task),
]
