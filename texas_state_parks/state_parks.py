from bs4 import BeautifulSoup

from datetime import datetime
from time import sleep
import subprocess
import sys

# INPUTS
POPCORN_NOTIFY_API_KEY = "REDACTED"
PHONE_NUMBER = "REDACTED"
RESERVATION_DATE = datetime(2020, 6, 20)
CURL_COMMAND = "REDACTED"

##

def notify(message):
    subprocess.run(f"""
        curl https://popcornnotify.com/notify \
        -u {POPCORN_NOTIFY_API_KEY}: \
        -d recipients="{PHONE_NUMBER}" \
        -d message="{message}" \
        -d subject="Texas State Parks"
        """, shell=True)
    print()

notify("Starting Texas State Parks notifier")

try:
    while True:
        if datetime.now() > RESERVATION_DATE:
            notify("Terminating notifier as too much time has elapsed")
            sys.exit(0)

        print(f"Making request at {datetime.now()}")
        request = subprocess.run(CURL_COMMAND, shell=True, capture_output=True)

        html = request.stdout
        soup = BeautifulSoup(html, 'html.parser')
        availability = soup.find("div", {"id": "avail1"}).attrs["title"]  # "Reserved" or "Available"
        print(f"Availability: {availability}")
        if availability not in ("Available", "Reserved"):
            raise Exception("Something went wrong")
        elif availability == "Available":
            notify("It's available!!!")
            notify("It's available!!!")
            notify("It's available!!!")
            sys.exit(0)

        sleep(60)
except KeyboardInterrupt:
    pass
except:
    notify("There was an error.")
