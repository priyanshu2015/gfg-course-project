from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from todo.helpers import task_status_update, update_obj
from todo.models import Task
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from todo.choices import StatusChoice
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, UpdateTaskForm

User = get_user_model()


# Create your views here.
@csrf_exempt
def register(request):
    if request.method == "GET":
        return render(
            request,
            template_name="todo/auth/register.html",
            context={"form": RegistrationForm()}
        )
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid() is False:
            return render(request, template_name="todo/auth/register.html", context={"form": form})
        # request_data = form.cleaned_data
        # username = request_data.get('username')
        # password = request_data.get('password')
        # email = request_data.get('email')
        form.save()
        return HttpResponse("Done")


@csrf_exempt
def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'todo/auth/login.html', {'form': form})
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                django_login(request, user)
                messages.success(request, f'Hi {username}, welcome back!')
                if request.GET.get("next") is not None:
                    return redirect(request.GET.get("next"))
                return redirect('/tasks/')
        print(form.errors)
        form.add_error('', "passwords do not match !")
        form.add_error('username', "passwords do not match !")
        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request,'todo/auth/login.html',{'form': form})


@login_required
def logout(request):
    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Not Found",
            "payload": {}
        }, status=404)
    django_logout(request)
    return JsonResponse({
        "status": "success",
        "message": "Successfully Logged Out",
        "payload": {}
    }, status=200)


@login_required
def list_create_task(request):
    if request.method == "POST":
        data = request.POST
        user = request.user
        title = data["title"]
        description = data.get("description", "")
        status = data.get("status", StatusChoice.PENDING)
        due_date = data.get("due_date", None)
        due_time = data.get("due_time", None)

        if due_date == "":
            due_date = None
        if due_time == "":
            due_time = None

        print(due_date)
        print(due_time)

        task = Task.objects.create(
            user=user,
            title=title,
            description=description,
            status=status,
            due_date=due_date,
            due_time=due_time
        )
        # task_serialized = serialize("json", [task], fields=('title', 'description', 'status', 'created_at', 'updated_at'))
        # return JsonResponse({
        #     "status": "success",
        #     "message": "Successfully created",
        #     "payload": json.loads(task_serialized)[0]
        # }, status=201)
        return redirect("/tasks/")
    if request.method == "GET":
        # list the objects
        page = request.GET.get("page", 1)
        search = request.GET.get("search", None)
        status = request.GET.get("status", None)
        ordering = request.GET.get("ordering", "-created_at")
        task_queryset = Task.objects.filter(user=request.user).order_by(ordering).prefetch_related("tags_new")

        if search is not None:
            task_queryset = task_queryset.filter(title__icontains=search)
        if status is not None:
            task_queryset = task_queryset.filter(status=status)

        # pagination
        # page_size = 5
        # paginator = Paginator(task_queryset, page_size)
        # try:
        #     page_obj = paginator.page(page)
        # except PageNotAnInteger:
        #     page_obj = paginator.page(1)
        # except EmptyPage:
        #     page_obj = paginator.page(paginator.num_pages)

        # # previous
        # if page_obj.has_previous():
        #     previous = page_obj.previous_page_number()
        # else:
        #     previous = ""
        # # next
        # if page_obj.has_next():
        #     next = page_obj.next_page_number()
        # else:
        #     next = ""

        # response_payload_results = serialize("json", page_obj.object_list)
        # return JsonResponse({
        #     "status": "success",
        #     "message": "Successfully retrieved",
        #     "payload": {
        #         "count": page_obj.paginator.count,
        #         "previous": previous,
        #         "next": next,
        #         "results": json.loads(response_payload_results)
        #     }
        # }, status=200)

        # print(page_obj.object_list)

        context = {
            "is_paginated": False,
            # "page_obj": page_obj,
            # "paginator": page_obj.paginator,
            # "results": page_obj.object_list
            "results": task_queryset
        }
        return render(request, template_name="todo/todo_list.html", context=context)
    else:
        return JsonResponse({
            "status": "error",
            "message": "Not Found",
            "payload": {}
        }, status=404)


@login_required
def retrieve_task(request, id):
    if request.method == "GET":
        task = Task.objects.filter(user=request.user, id=id).first()
        if task is None:
            response_data = {
                "status": "error",
                "message": "Task with this id not found",
                "payload": {}
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        task_serialized = serialize("json", [task], fields=('title', 'description', 'status', 'created_at', 'updated_at'))
        return JsonResponse({
            "status": "success",
            "message": "Successfully retrieved",
            "payload": json.loads(task_serialized)[0]
        }, status=200)


@login_required
def update_task(request, id):
    if request.method == "GET":
        task = Task.objects.filter(user=request.user, id=id).first()
        if task is None:
            return HttpResponse("Not Found")
        context_data = {
            "form": UpdateTaskForm(instance=task)
        }
        return render(request, template_name="todo/update_task.html", context=context_data)
    if request.method == "POST":
        task = Task.objects.filter(user=request.user, id=id).first()
        if task is None:
            return HttpResponse("Not Found")
        form = UpdateTaskForm(request.POST, instance=task)

        if form.is_valid():
            status = form.cleaned_data.get("status")

            if status is not None:
                task_status_update(task=task, status=status)
            form.save()
            messages.success(request=request, message="Successfully Updated")
            return redirect("/tasks/")
        else:
            context_data = {"form": form}
            return render(request, template_name="todo/update_task.html", context=context_data)


@login_required
def delete_task(request, id):
    if request.method != "POST":
        messages.error(request=request, message="Not Found")
        # return HttpResponse("Not Found")
        return redirect("/tasks/")
    task = Task.objects.filter(user=request.user, id=id).first()
    if task is None:
        return HttpResponse("Not Found")
    task.delete()
    return redirect(reverse("list-create-task"))