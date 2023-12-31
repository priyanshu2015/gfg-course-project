# Generated by Django 4.2.6 on 2023-10-29 12:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_useradditional_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomPermission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "permissions": (
                    ("view_operations_dashboard", "can view operations dashboard"),
                    ("perform_transfers", "can perform transfers"),
                ),
                "managed": False,
                "default_permissions": {},
            },
        ),
    ]
