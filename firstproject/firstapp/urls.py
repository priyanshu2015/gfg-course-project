from django.urls import path
from .views import start

urlpatterns = [
    path("start/", start),
]
