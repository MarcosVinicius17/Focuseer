import subprocess


def send_notification(title, message):
    subprocess.run(["notify-send", title, message])


send_notification("Hello, World!", "This is a test notification")
