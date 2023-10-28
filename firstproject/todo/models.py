from django.db import models
from todo.choices import StatusChoice
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    status = models.CharField(choices=StatusChoice.CHOICE_LIST, max_length=16)
    # null => controls the nullability at database level
    # blank => controls the nullability at application level
    due_date = models.DateField(blank=True, null=True)
    due_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # usage of DjangoJSONEncoder?
    extras = models.JSONField(default=dict, encoder=DjangoJSONEncoder)

    # tags = models.ManyToManyField(Tag, related_name="tasks")
    tags_new = models.ManyToManyField(Tag, related_name="tasks", through='TaskTag')

    def __str__(self) -> str:
        return self.title


class TaskTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tag_id", "task_id"],
                name="unique_task_tag",
            )
        ]

