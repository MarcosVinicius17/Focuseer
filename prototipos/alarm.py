import datetime, time, subprocess


# Set the alarm time (in 24-hour format)
alarm_time = "18:24"

# Convert the alarm time to a datetime object
alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M")

while True:
    # Get the current time
    current_time = datetime.datetime.now()

    # Check if it is time for the alarm
    if current_time.strftime("%H:%M") == alarm_time.strftime("%H:%M"):
        print("baka")
        subprocess.run(["notify-send", "Make me Focus", "Alarm!"])
        # Exit the program
        break

    # Sleep for 1 second
    time.sleep(1)
