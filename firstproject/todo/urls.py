from django.urls import path
from .views import login, list_create_task, retrieve_update_delete_task, register, logout

urlpatterns = [
    path("login/", login),
    path("logout/", logout),
    path("signup/", register),
    path("tasks/", list_create_task),
    path("tasks/<int:id>/", retrieve_update_delete_task),
]
