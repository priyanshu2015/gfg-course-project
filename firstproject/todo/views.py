from django.shortcuts import render
from todo.helpers import get_404_json_response, update_object
from .choices import TaskStatusChoice
from django.http import HttpResponse, JsonResponse
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize

User = get_user_model()


def register(request):
    if request.method != "POST":
        return get_404_json_response()
    request_data = json.loads(request.body)
    username = request_data.get('username', None)
    password = request_data.get('password', None)
    email = request_data.get('email', None)

    if username is None or password is None or email is None:
        return JsonResponse(
        {
            "status": "error",
            "message": "Please provide necessary details",
            "payload": {}
        }, status=400
    )

    existing_user = User.objects.filter(username=username)
    if existing_user.exists():
        return JsonResponse(
            {
                "status": "error",
                "message": "User with this username already exists",
                "payload": {}
            }, status=400
        )

    user = User(
        email=email, username=username
    )
    user.set_password(raw_password=password)
    user.save()
    return JsonResponse(
        {
            "status": "success",
            "message": "Successfully Registered",
            "payload": {
                "email": user.email,
                "username": user.username
            }
        }, status=200
    )


@csrf_exempt
def login(request):
    if request.method != "POST":
        return get_404_json_response()
    request_data = json.loads(request.body)
    username = request_data.get('username', None)
    password = request_data.get('password', None)

    user = authenticate(username=username, password=password)

    if user is not None:
        django_login(request, user)
        return JsonResponse(
            {
                "status": "success",
                "message": "Successfully logged in",
                "payload": {
                    "email": user.email,
                    "username": user.username
                }
            }, status=200
        )
    else:
        return JsonResponse({
            "status": "error",
            "message": "Invalid Credentials",
            "payload": {}
        }, status=400)


@login_required
def logout(request):
    if request.method != "POST":
        return get_404_json_response()
    if request.user is None:
        return JsonResponse({
            "status": "error",
            "message": "Please login first",
            "payload": {}
        }, status=400)
    django_logout(request)
    return JsonResponse(
        {
            "status": "success",
            "message": "Successfully logged out",
            "payload": {}
        }, status=200
    )


@login_required
def list_create_task(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        title = data.get("title")
        description = data.get("description", "")
        status = data.get("status", TaskStatusChoice.PENDING)
        due_date = data.get("")
        task = Task.objects.create(
            user=user,
            title=title,
            description=description,
            status=status,
            due_date=due_date
        )
        return JsonResponse(
            {
                "status": "success",
                "message": "Successfully Created",
                "payload": {
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "due_date": task.due_date,
                    "due_time": task.due_time,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at
                }
            },
            status=201
        )
    elif request.method == "GET":
        page = request.GET.get("page", 1)
        ordering = request.GET.get("ordering", "-created_at")
        search = request.GET.get("search", None)
        status = request.GET.get("status", None)
        task_queryset = Task.objects.filter(user=request.user).order_by(ordering)
        if search is not None:
            task_queryset = task_queryset.filter(title__icontains=search)
        if status is not None:
            task_queryset = task_queryset.filter(status=status)

        # pagination
        page_size = 1
        paginator = Paginator(task_queryset, page_size)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        if page_obj.has_previous():
            previous = page_obj.previous_page_number()
        else:
            previous = ""
        if page_obj.has_next():
            next = page_obj.next_page_number()
        else:
            next = ""

        response_payload_results = serialize("json", page_obj.object_list, fields=('title', 'description', 'user'))
        # The safe boolean parameter defaults to True. If it's set to False, any object can be passed for serialization (otherwise only dict instances are allowed).
        joins = ["user"]
        return JsonResponse({
            "status": "succes",
            "message": "Successfully fetched all tasks",
            "payload": {
                "count": page_obj.paginator.count,
                "previous": previous,
                "next": next,
                "results": json.loads(response_payload_results)
            }
        }, status=200)

        # text/html
        # return HttpResponse(response_payload_results, content_type="application/json")
    else:
        return JsonResponse(
            {
                "status": "error",
                "message": "Not Found",
                "payload": {}
            },
            status=404
        )


@login_required
def retrieve_update_delete_task(request, id):
    if request.method == "GET":
        task = Task.objects.filter(user=request.user, id=id).first()
        if task is None:
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Task with {id} id does not exists",
                    "payload": {}
                },
                status=404
            )
        task_serialized = serialize("json", [task], fields=('title', 'description', 'user'))
        return JsonResponse({
            "status": "succes",
            "message": "Successfully retrieved the task",
            "payload": json.loads(task_serialized)[0]
        }, status=200)

    if request.method in ["PATCH", "PUT"]:
        data = json.loads(request.body)
        # tasks = Task.objects.filter(user=request.user, id=id)
        # task = tasks.first()
        task = Task.objects.filter(user=request.user, id=id).first()
        if task is None:
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Task with {id} id does not exists",
                    "payload": {}
                },
                status=404
            )
        update_object(task, **data)
        # tasks.update(**data)
        return JsonResponse(
            {
                "status": "error",
                "message": f"Task with {id} id updated successfully",
                "payload": {
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "due_date": task.due_date,
                    "due_time": task.due_time,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at
                }
            },
            status=200
        )
    elif request.method == "DELETE":
        task = Task.objects.filter(user=request.user, id=id).first()
        if task is None:
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Task with {id} id does not exists",
                    "payload": {}
                },
                status=404
            )
        task.delete()
        return JsonResponse(
                {
                    "status": "success",
                    "message": f"Task with {id} id deleted successfully",
                    "payload": {}
                },
                status=200
            )
    else:
        return JsonResponse(
            {
                "status": "error",
                "message": "Not Found",
                "payload": {}
            },
            status=404
        )


# what is missing => request body validation, response validation and customization, unexpected error handling, throttling, removing csrf and adding cors origin, controlling response using global renderers, stateless authentication