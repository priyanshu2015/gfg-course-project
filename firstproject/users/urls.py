from django.urls import path
from .views import view_operations_dashboard

urlpatterns = [
    path("dashboard/", view_operations_dashboard),
]
