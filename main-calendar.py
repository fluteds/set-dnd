import requests
from datetime import datetime
import json
from icalendar import Calendar, Event
import logging
from pytz import timezone
import time

#logging.basicConfig(filename='logs/error.log', level=logging.ERROR)
log_prefix = "[" + datetime.now().strftime("%I:%M %p") + "]"
current_time = datetime.now(timezone("GMT"))

# Load config from file
with open("config.json", "r") as f:
    config = json.load(f)

# Retrieve calendar data
try:
    response = requests.get(config["calendar_url"])
    calendar_data = response.text
    print(log_prefix + " Successfully found the calendar.")
    print(log_prefix + " Attempting to pull calendar data.")
except requests.exceptions.RequestException as e:
    logging.ERROR(" Failed to find the calendar. Check the provided URL.")
    logging.ERROR(e)

# Create a calendar object from the data
calendar = Calendar.from_ical(calendar_data)

events_printed = False

# Extract event data
events_data = []
new_events = []
for component in calendar.walk():
    if component.name == "VEVENT":
        event = Event.from_ical(component.to_ical())
        start_time = event.get('dtstart').dt
        end_time = event.get('dtend').dt
        summary = event.get('summary')
        events_data.append({
            "subject": summary,
            "start_time": start_time,
            "end_time": end_time
        })

# Print events data (debug)
#print(events_data)

# Find today's events
today_events = []
for event in events_data:
    event_date = event["start_time"].date().strftime("%d/%m/%Y")
    if event_date == current_time.strftime("%d/%m/%Y"):
        today_events.append(event)
        
# Sort events
events_data = sorted(events_data, key=lambda x: (datetime.strptime(x["start_time"].strftime("%d/%m/%Y"), '%d/%m/%Y'), x["start_time"].time()))

# Save events to text file
with open("data/events.txt", "w") as f:
    for event in events_data:
        start_time = event["start_time"].strftime("%Y-%m-%d %H:%M:%S")
        end_time = event["end_time"].strftime("%Y-%m-%d %H:%M:%S")
        date = event["start_time"].strftime("%d/%m/%Y")
        f.write("{} - {} - Start Time: {} - End Time: {}\n".format(event["subject"],date, start_time, end_time))
    print(log_prefix + " Successfully wrote events to events.txt")
    
if not today_events:
    print()
    print(log_prefix + " There is not an event scheduled for today.")
    print()

if len(today_events) > 1:
    print()
    print("EVENTS FOR TODAY")
    print()
    for event in today_events:
        start_time = event["start_time"].   strftime("%Y-%m-%d %H:%M:%S")
        end_time = event["end_time"].strftime("%Y-%m-%d %H:%M:%S")
        print(f'{event["subject"]} - Start Time: {start_time} - End Time: {end_time}')
        
elif len(today_events) == 1:
    # Print today's events
    for event in today_events:
        start_time = event["start_time"].strftime("%Y-%m-%d %H:%M:%S")
        end_time = event["end_time"].strftime("%Y-%m-%d %H:%M:%S")
        print()
        print("EVENTS FOR TODAY")
        print()
        print(f'{event["subject"]} - Start Time: {start_time} - End Time: {end_time}')
        print()
        
# Update Discord Status
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

# Check Discord Status
def check_status():
    headers = {
        "Authorization": config["discord_token"],
    }
    response = requests.get("https://discord.com/api/v6/users/@me/settings", headers=headers)
    if response.status_code == 200 and response.ok:
        data = response.json()
        #print(data) # Prints the data return
        return data["status"]
    else:
        logging.ERROR("Failed to check Discord status, status code: {}".format(response.status_code))
        logging.ERROR(response.text)
                    
if today_events:
    # Check current status
    current_status = check_status()

    # Only update status if it is not already set to "idle"
    if current_status != "idle":
        update_status("idle")
        print(log_prefix + " Successfully set Discord status to idle.")
    else:
        print(log_prefix + " Discord status is already set to idle. No status change.")

def main():
    while True:
        # Define timezone
        current_time = datetime.now(timezone("GMT"))
        
        # Check if there's an ongoing event
        ongoing_event = None
        for event in events_data:
            if event["start_time"] <= current_time <= event["end_time"]:
                ongoing_event = event

        # Update status accordingly
        if ongoing_event:
            if current_status != "dnd":
                update_status("dnd")
                print(log_prefix + " Changed status to dnd for: {}".format(ongoing_event["subject"]))
            else:
                print(log_prefix + " Status is already dnd for: {}".format(ongoing_event["subject"]) + " Skipping status change.")
        #else:
            #update_status("idle")
            #print(log_prefix + " Changed status to idle. | No ongoing event.") 

        # Pause the script for x seconds before checking for events again
        print(log_prefix + " Waiting for 120 seconds to check event status again.")
        time.sleep(120)

if __name__ == "__main__":
    main()
