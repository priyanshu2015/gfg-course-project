from django.urls import path
from .views import login, list_create_task, register, logout, retrieve_update_task, delete_task

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("signup/", register, name="signup"),
    path("tasks/", list_create_task, name="list-create-task"),
    path("tasks/delete/<int:id>/", delete_task, name="delete-task"),
    path("tasks/<int:id>/", retrieve_update_task, name="retrieve-update-task"),
]
