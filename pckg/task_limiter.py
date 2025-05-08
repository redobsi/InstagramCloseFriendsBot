import os
import json
import sys
from colorama import Fore, Style

LIMIT = 100
TRACK_FILE = os.path.join(os.path.expanduser("~"), ".my_app_usage.json")

def load_count():
    if not os.path.exists(TRACK_FILE):
        return 0
    try:
        with open(TRACK_FILE, "r") as f:
            data = json.load(f)
        return data.get("count", 0)
    except:
        return 0

def save_count(count):
    with open(TRACK_FILE, "w") as f:
        json.dump({"count": count}, f)

def increment_task():
    count = load_count()
    if count >= LIMIT:
        print(Fore.RED + Style.BRIGHT + "Task limit reached. Please contact support." + Style.RESET_ALL)
        sys.exit()
    count += 1
    save_count(count)
