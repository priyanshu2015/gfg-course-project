from django.urls import path
from .views import register, login, logout, list_create_task, retrieve_update_task, delete_task

urlpatterns = [
    path("signup/", register),
    path("login/", login),
    path("logout/", logout),
    # POST => Create, GET => List Tasks
    path("tasks/", list_create_task, name="list-create-task"),
    path("tasks/delete/<int:id>/", delete_task, name="delete-task"),
    path("tasks/<int:id>/", retrieve_update_task),
]
