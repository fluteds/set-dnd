
import requests
from datetime import datetime
#import schedule
import time
import json

with open("config.json", "r") as f:
    config = json.load(f)
    
dnd_time = ("17:00:00", "22:00:00") # Change times to be in DND here

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
    if datetime.strptime(dnd_time[0], "%H:%M:%S").time() <= current_time <= datetime.strptime(dnd_time[1], "%H:%M:%S").time():
        current_status = check_status()
        if current_status != "dnd":
            status = update_status("dnd")
            if "status" in status:
                print(log_prefix + " Within DND period. Successfully updated status to do not disturb.")
        else:
            print(log_prefix + " Status unchanged. (Already DND.)")
    else:
        current_status = check_status()
        if current_status != "idle":
            status = update_status("idle")
            if "status" in status:
                print(log_prefix + " Successfully updated status to idle.")
        else:
            print(log_prefix + " Status unchanged. (Already idle.)")

#schedule.every().day.at(dnd_time[0]).do(update_status, "dnd") # set status to do not disturb at start time
#schedule.every().day.at(dnd_time[1]).do(update_status, "idle") # set status to idle at end time

while True:
    main()
    time.sleep(300) # delay for 5 minutes before checking again