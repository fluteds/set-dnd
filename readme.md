# Set DND

A simple self bot that updates your Discord status to "Do Not Disturb" based on your calendar events. It retrieves your calendar data from a specified public url, filters through the events, saves them to a text file and checks if the current time falls within any event start and end times. If it does, the script updates your Discord status to "Do Not Disturb" and also changes back to "Idle" when the event ends.

## Setting up

- Install `requrements.txt`

Create a `config.json` file with the following keys:

- `discord_token`: Account token
- `calendar_url`: URL of your public internet calendar
- `timezone`: EG. [Europe/London](https://timezonedb.com/time-zones)

## What if I don't have a calendar?

If you want to set your status to "Do Not Disturb" at a set time each day, use the other script (`main.py`) which can be left to run on a task scheduler or cron job. By default these "Do Not Disturb" hours are between 5pm and 10pm and the status will set to "Idle" outside of those hours. You can change these times by editing `dnd_time` accordingly.

## Will I get banned?

Maybe. This is classified as a self bot because of the status changing and goes against Discord's terms of service but I haven't seen users actively get banned for status changing so use at your own risk on an account you don't that much care for and don't run it too often as that will spam the API.

## Disclaimer

I am not responsible for any token losses from your own practices. This script does not store any of your information outside of the config. You should be keeping your tokens safe just like bank card details. Once someone has your token they have access to your whole account. If you cannot work out how to use this script from the config and don't know how to get your own Discord token, this is not for you.
