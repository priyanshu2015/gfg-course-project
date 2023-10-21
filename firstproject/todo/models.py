from django.db import models
from todo.choices import TaskStatusChoice
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    status = models.CharField(choices=TaskStatusChoice.CHOICE_LIST, max_length=16)
    due_date = models.DateField(blank=True, null=True)
    due_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title