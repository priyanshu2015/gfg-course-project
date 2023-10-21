from django.urls import path
from .views import start, check_concurrency

urlpatterns = [
    path("start/", start),
    path("check-concurrency/", check_concurrency),
]
