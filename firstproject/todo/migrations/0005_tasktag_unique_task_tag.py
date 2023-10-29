# Generated by Django 4.2.6 on 2023-10-28 09:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0004_remove_task_tags_tasktag_task_tags_new"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="tasktag",
            constraint=models.UniqueConstraint(
                fields=("tag_id", "task_id"), name="unique_task_tag"
            ),
        ),
    ]