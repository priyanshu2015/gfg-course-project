from .models import Task
from django.utils import timezone


def update_obj(obj, **kwargs):
    for k, v in kwargs.items():
        if v is not None:
            setattr(obj, k, v)
    obj.save()


# [{"status_from": "Pending", "status_to": "In_Progress", "timestamp"}, {}]


def task_status_update(task: Task, status: str):
    if task.status == status:
        return
    status_history = task.extras.get("status_history", None)
    if status_history is None:
        task.extras = {"status_history": []}
        status_history = []
    status_history.append({
        "status_from": task.status,
        "status_to": status,
        "timestamp": timezone.now().timestamp()
    })
    task.status = status
    task.extras["status_history"] = status_history
    task.save()