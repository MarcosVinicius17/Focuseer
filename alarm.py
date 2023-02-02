import gi, datetime, subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

"""
Obter a hora pelas labels de horas e minutos
"""

"""
Trabalhar com 2 casas decimais
Fazer uma label editável (apenas números e verificar 24 horas e 60 minutos)
"""


def increment_hour(button) -> None:
    current_hour = int(lblHours.get_text())
    current_hour += 1
    if current_hour == 24:
        current_hour = 0
    lblHours.set_text(str(current_hour))


def decrement_hour(button) -> None:
    current_hour = int(lblHours.get_text())
    current_hour -= 1
    if current_hour == -1:
        current_hour = 23
    lblHours.set_text(str(current_hour))


def increment_minute(button) -> None:
    current_minute = int(lblMinutes.get_text())
    current_minute += 1
    if current_minute == 60:
        current_minute = 0
    lblMinutes.set_text(str(current_minute))


def decrement_minute(button) -> None:
    current_minute = int(lblMinutes.get_text())
    current_minute -= 1
    if current_minute == -1:
        current_minute = 59
    lblMinutes.set_text(str(current_minute))


def alarm(button):

    runs = 0

    alarm_time = "00:00"
    alarm_hour = lblHours.get_text()
    alarm_minute = lblMinutes.get_text()

    alarm_time = alarm_hour + ":" + alarm_minute
    alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M")
    print(f"alarm set for {alarm_time}")
    while True:
        current_time = datetime.datetime.now()
        if current_time.strftime("%H:%M") == alarm_time.strftime("%H:%M"):
            if runs < 1:
                subprocess.run(["notify-send", "Make me Focus", "Alarm!"])
                runs += 1
            if runs == 1:
                break


builder = Gtk.Builder()
builder.add_from_file("alarm.glade")

window = builder.get_object("Window")


btnAlarm = builder.get_object("btnAlarm")
btnAlarm.connect("clicked", alarm)

btnHourMinus = builder.get_object("btnHourMinus")
btnHourPlus = builder.get_object("btnHourPlus")

btnMinuteMinus = builder.get_object("btnMinuteMinus")
btnMinutePlus = builder.get_object("btnMinutePlus")

lblHours = builder.get_object("lblHours")
lblMinutes = builder.get_object("lblMinutes")


btnHourMinus.connect("clicked", decrement_hour)
btnHourPlus.connect("clicked", increment_hour)
btnMinuteMinus.connect("clicked", decrement_minute)
btnMinutePlus.connect("clicked", increment_minute)


window.show_all()

Gtk.main()
