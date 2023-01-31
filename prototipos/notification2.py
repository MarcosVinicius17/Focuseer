import dbus


def send_notification(title, message):
    bus = dbus.SessionBus()
    notify_obj = bus.get_object(
        "org.freedesktop.Notifications", "/org/freedesktop/Notifications"
    )
    interface = dbus.Interface(notify_obj, "org.freedesktop.Notifications")
    interface.Notify("", 0, "", title, message, [], {}, 0)


send_notification("Hello, World!", "This is a test notification")
