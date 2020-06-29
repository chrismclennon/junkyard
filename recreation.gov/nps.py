from datetime import datetime
from time import sleep
import subprocess
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

DATES = [
    "Saturday, July 4, 2020",
    "Sunday, July 5, 2020",
    "Monday, July 6, 2020",
    "Tuesday, July 7, 2020",
    "Wednesday, July 8, 2020",
]
TIMES = [
    "6:00 AM",
    "8:00 AM",
    "10:00 AM",
]
EXCLUDE = [
    ("Saturday, July 4, 2020", "6:00 AM"),
    ("Saturday, July 4, 2020", "8:00 AM"),
]

POPCORN_NOTIFY_API_KEY = "REDACTED"
PHONE_NUMBER = "REDACTED"

def notify(message):
    subprocess.run(f"""
        curl https://popcornnotify.com/notify \
        -u {POPCORN_NOTIFY_API_KEY}: \
        -d recipients="{PHONE_NUMBER}" \
        -d message="{message}" \
        -d subject="Subject"
        """, shell=True)
    print()

def run():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.recreation.gov/ticket/facility/300013?q=Rocky%20Mountain%20National%20Park%20Timed%20Entry")

    while True:
        if datetime.now() > datetime(2020, 7, 2):
            notify("Stopping NPS notifier due to late date")
            driver.close()
            sys.exit(0)
        print(f"\nExecuting a run at {datetime.now()}")

        #
        # Click on "Private Vehicle Entrance"
        tour_options = driver.find_element_by_id("tour-options").find_elements_by_tag_name("option")
        for option in tour_options:
            if option.get_attribute("value") == "2078":
                option.click()
                break

        #
        # Click on "Annual Lifetime/Pass Holder"
        guest_counter = driver.find_element_by_id("guest-counter")
        guest_counter.click()
        driver.find_element_by_xpath('//*[@id="guest-counter-popup"]/div/div[1]/div/div/div[2]/div[2]/div/div/button[2]').click()
        guest_counter.click()

        #
        # Click on dates on calendar
        for date in DATES:
            calendar = driver.find_element_by_id("selectTourDatePicker")
            calendar.click()
            datebox = driver.find_element_by_css_selector(f'td[aria-label^="{date}"]')
            datebox.click()
            driver.find_element_by_xpath('//*[@id="page-content"]/div/div/div[1]/div[2]/div/div/div[2]/div/div[1]/div/div[2]/div/fieldset/div/div[4]/div/button').click()

            for time in TIMES:
                exclude_tuple = (date, time)
                if exclude_tuple in EXCLUDE:
                    print(f"Excluding {date} and {time}...")
                    continue

                print(f"Checking {date} and {time}...")
                availability = driver.find_element_by_css_selector(f'button[title="{time}"]').get_attribute("aria-label")
                if "Available" in availability:
                    msg = f"RMNP is available on {date} at {time}"
                    print(msg)
                    notify(msg)
                    sys.exit(0)
        print("Sleeping for 60 seconds...")
        sleep(60)
        driver.refresh()


while True:
    try:
        run()
    except KeyboardInterrupt:
        driver.close()
        sys.exit(0)
    except Exception as e:
        print(e)

driver.close()
