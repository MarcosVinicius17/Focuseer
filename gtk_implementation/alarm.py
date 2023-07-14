import gi, datetime, subprocess, threading

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from playsound import playsound


def increment_hour(button) -> None:
    current_hour = int(entryHours.get_text())
    current_hour += 1
    if current_hour >= 24:
        current_hour = "00"
    entryHours.set_text(str(current_hour))


def decrement_hour(button) -> None:
    current_hour = int(entryHours.get_text())
    current_hour -= 1
    if current_hour == -1:
        current_hour = "23"
    entryHours.set_text(str(current_hour))


def increment_minute(button) -> None:
    current_minute = int(entryMinutes.get_text())
    current_minute += 1
    if current_minute == 60:
        current_minute = "00"
    entryMinutes.set_text(str(current_minute))


def decrement_minute(button) -> None:
    current_minute = int(entryMinutes.get_text())
    current_minute -= 1
    if current_minute == -1:
        current_minute = "59"
    entryMinutes.set_text(str(current_minute))


def validate_hour(entry) -> None:
    text = entry.get_text()
    if len(text) == 1:
        entry.set_text("0" + text)
    if text.isdigit():
        hour = int(text)
        if hour < 0 or hour > 23:
            entry.set_text("23")


def validate_minute(entry) -> None:
    text = entry.get_text()
    if len(text) == 1:
        entry.set_text("0" + text)
    if text.isdigit():
        minute = int(text)
        if minute < 0 or minute > 59:
            entry.set_text("59")


def start_alarm(button) -> None:
    thread = threading.Thread(target=alarm)
    thread.start()


"""def alarm() -> None:
    runs = 0

    alarm_time = "00:00"
    alarm_hour = entryHours.get_text()
    alarm_minute = entryMinutes.get_text()

    alarm_time = alarm_hour + ":" + alarm_minute
    alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M")
    print(f"Alarm set for {alarm_time}")
    while True:
        current_time = datetime.datetime.now()
        if current_time.strftime("%H:%M") == alarm_time.strftime("%H:%M"):
            if runs < 1:
                subprocess.run(["notify-send", "Focuseer", "Seu alarme"])
                mp3_file = (
                    "/home/marcos/Desktop/UNIP/tcc/nao_programacao/sounds/alarm.mp3"
                )
                playsound(mp3_file)

                runs += 1
            if runs == 1:
                break"""


def alarm() -> None:
    runs = 0

    alarm_time = "00:00"
    alarm_hour = entryHours.get_text()
    alarm_minute = entryMinutes.get_text()

    alarm_time = alarm_hour + ":" + alarm_minute
    alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M")
    print(f"Alarm set for {alarm_time}")
    while True:
        current_time = datetime.datetime.now()
        if current_time.strftime("%H:%M") == alarm_time.strftime("%H:%M"):
            if runs < 1:
                if chkAlarm.get_active():
                    subprocess.run(["notify-send", "Focuseer", "Seu alarme"])
                    runs += 1
                else:
                    subprocess.run(["notify-send", "Focuseer", "Seu alarme"])
                    mp3_file = (
                        "/home/marcos/Desktop/UNIP/tcc/nao_programacao/sounds/alarm.mp3"
                    )
                    playsound(mp3_file)
                    runs += 1
            if runs == 1:
                break


builder = Gtk.Builder()
builder.add_from_file("glade_screens/alarm.glade")

window = builder.get_object("Window")


btnAlarm = builder.get_object("btnAlarm")
btnAlarm.connect("clicked", start_alarm)

btnHourMinus = builder.get_object("btnHoursMinus")
btnHourPlus = builder.get_object("btnHoursPlus")

btnMinuteMinus = builder.get_object("btnMinuteMinus")
btnMinutePlus = builder.get_object("btnMinutePlus")

entryHours = builder.get_object("hours")
entryMinutes = builder.get_object("minutes")

# Valida as entradas dos GtkEntry via teclado
entryHours.connect("changed", validate_hour)
entryMinutes.connect("changed", validate_minute)

chkAlarm = builder.get_object("chkAlarm")


btnHourMinus.connect("clicked", decrement_hour)
btnHourPlus.connect("clicked", increment_hour)
btnMinuteMinus.connect("clicked", decrement_minute)
btnMinutePlus.connect("clicked", increment_minute)

# CSS
css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)

context_window = window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_hours_plus = btnHourPlus.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_hours_minus = btnHourMinus.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_minute_plus = btnMinutePlus.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_minute_minus = btnMinuteMinus.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_entry_hours = entryHours.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_entry_minutes = entryMinutes.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


window.show_all()

Gtk.main()
