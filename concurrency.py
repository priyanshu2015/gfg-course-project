import time
import os
import threading

def test():
    print("START PID", os.getpid(), "TID", threading.get_native_id())
    time.sleep(5)
    print("STOP  PID", os.getpid(), "TID", threading.get_native_id())


# python manage.py runserver --nothreading
# chrome browser send requests to same url by "single thread", not the django development server handle requests by single thread

