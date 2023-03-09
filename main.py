
import requests
from datetime import datetime
import schedule
import time
import json

# TODO (maybe?)
# add custom emojis and text from a file at random when run

with open("config.json", "r") as f:
    config = json.load(f)

def update_status(status):
    """
    Update the Discord status with the specified status

    Args:
        status (str): The new status ("online", "idle", "dnd", or "invisible")

    Returns:
        data (any): The Discord response
    """
    url = "https://discord.com/api/v6/users/@me/settings"
    headers = {
        "Authorization": config["discord_token"],
        "Content-Type": "application/json",
    }
    payload = {
            "status": status,
            "afk": False
    }
    response = requests.patch(url, json=payload, headers=headers)
    data = response.json()
    return data

def check_status():
    headers = {
        "Authorization": config["discord_token"],
    }
    response = requests.get("https://discord.com/api/v6/users/@me/settings", headers=headers)
    data = response.json()
    return data["status"]

def main():
    log_prefix = "[" + datetime.now().strftime("%I:%M %p") + "]"
    current_time = datetime.now().time()
    if datetime.strptime("17:00:00", "%H:%M:%S").time() <= current_time <= datetime.strptime("22:00:00", "%H:%M:%S").time():
        current_status = check_status()
        if current_status != "dnd":
            status = update_status("dnd")
            if "status" in status:
                print(log_prefix + " Successfully updated status to do not disturb.")
    else:
        current_status = check_status()
        if current_status != "idle":
            status = update_status("idle")
            if "status" in status:
                print(log_prefix + " Successfully updated status to idle.")
        else:
            print(log_prefix + " Not updating status. Current status is already idle.")

schedule.every().day.at("16:59").do(update_status)
schedule.every().day.at("22:01").do(update_status)

while True:
    main()
    time.sleep(300) # delay for 5 minutes before checking again