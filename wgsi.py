import os
import threading
import requests
import time

from dj_static import Cling
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mahjong-matching.settings")

application = Cling(get_wsgi_application())

def awake():
    while True:
        try:
            print("Start Awaking")
            requests.get("https://mahjong-matching.herokuapp.com/")
            print("End")
        except:
            print("error")
        time.sleep(300)

t = threading.Thread(target=awake)
t.start()
