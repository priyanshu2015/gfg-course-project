from django.shortcuts import render
import os
import threading
import time

# Create your views here.
from django.http import HttpResponse
from firstapp.models import Account

def start(request):
    # business logic
    a = Account.objects.create(
        amount=10,
        currency="inr"
    )
    a_fetched = Account.objects.all()
    print(a_fetched)
    return HttpResponse("Hello")


def check_concurrency(request):
    print("START PID", os.getpid(), "TID", threading.get_native_id())
    time.sleep(5)
    print("STOP  PID", os.getpid(), "TID", threading.get_native_id())
    return HttpResponse("Done")

