from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = "Create a normal user"

    def handle(self, *args, **kwargs):
       print(timezone.now())