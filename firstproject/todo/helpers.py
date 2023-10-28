from django.utils import timezone


def update_obj(obj, **kwargs):
    for k, v in kwargs.items():
        if v is not None:
            setattr(obj, k, v)
    obj.save()


def task_status_update(task, status: str):
    if task.status == status:
        return
    status_history = task.extras.get("status_history")
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