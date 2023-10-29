from django.shortcuts import render
from django.http import HttpResponse
from .decorators import group_required
from django.contrib.contenttypes.models import ContentType
from todo.models import Task
from django.contrib.auth.decorators import permission_required

# Create your views here.

# @group_required(group="operations")
@permission_required(perm="users.view_operations_dashboard")
def view_operations_dashboard(request):
    # if request.user.groups.filter(name="operations").exists() is False:
    #     return HttpResponse("Not Found")

    # ct = ContentType.objects.get_for_model(Task)
    # if request.user.user_permissions.filter(codename="view_task", content_type=ct).exists() is False:
    #     return HttpResponse("Not Found")
    # if request.user.has_perms(("todo.view_task",)) is False:
    #     return HttpResponse("Not Found")
    return HttpResponse("Operations Dashboard")