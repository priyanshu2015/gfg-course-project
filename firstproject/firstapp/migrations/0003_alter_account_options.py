# Generated by Django 4.2.6 on 2023-10-29 12:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("firstapp", "0002_account_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="account",
            options={
                "permissions": (
                    ("can_make_transfers", "can make transfers"),
                    ("can_deposit_funds", "can deposit funds"),
                )
            },
        ),
    ]
