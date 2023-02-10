import gi, datetime, subprocess, time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

"""
Trabalhar com 2 casas decimais
Fazer uma label editável (apenas números e verificar 24 horas e 60 minutos)
"""

"""
Methods
"""

"""
Calculate the total time in seconds, then go decreasing while updating the GUI
"""


"""def timer(button):
    current_hour = int(lblHours.get_text())
    current_minute = int(lblMinutes.get_text())
    current_second = int(lblSeconds.get_text())
    total_seconds = current_second + 60 * (current_minute + 60 * current_hour)
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        time_remaining = total_seconds - elapsed_time
        print(f"Time remaining: {int(time_remaining)} seconds")
        if elapsed_time >= total_seconds:
            break
        time.sleep(1)
"""


def timer(button) -> None:
    current_hour = int(lblHours.get_text())
    current_minute = int(lblMinutes.get_text())
    current_second = int(lblSeconds.get_text())

    total_time_seconds = current_second + (current_minute * 60) + (current_hour * 3600)

    # print(f"Total of {total_time_seconds} seconds")

    starting_time = time.time()

    while True:
        time_spend = time.time() - starting_time
        time_remaining = total_time_seconds - time_spend
        print(f"Time remaining: {int(time_remaining)} seconds")
        #decrement_second_timer()
        if time_spend >= total_time_seconds:
            print("time is over")
            lblSeconds.set_text("00")
            break
        time.sleep(1)


"""
There is definetely a better way than this, but this is a problem to future me
"""


def decrement_hour_timer() -> None:
    current_hour = int(lblHours.get_text())
    current_hour -= 1
    if current_hour == -1:
        current_hour = 23
    lblHours.set_text(str(current_hour))


def decrement_minute_timer() -> None:
    current_minute = int(lblMinutes.get_text())
    current_minute -= 1
    if current_minute == -1:
        current_minute = 59
    lblMinutes.set_text(str(current_minute))


def decrement_second_timer() -> None:
    current_second = int(lblSeconds.get_text())
    current_second -= 1
    if current_second == -1:
        current_second = 59
    lblSeconds.set_text(str(current_second))


"""
Methods with button
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


def increment_second(button) -> None:
    current_second = int(lblSeconds.get_text())
    current_second += 1
    if current_second == 60:
        current_second = 0
    lblSeconds.set_text(str(current_second))


def decrement_second(button) -> None:
    current_second = int(lblSeconds.get_text())
    current_second -= 1
    if current_second == -1:
        current_second = 59
    lblSeconds.set_text(str(current_second))


"""
Getting the objects
"""
builder = Gtk.Builder()
builder.add_from_file("timer.glade")

window = builder.get_object("Window")

btnHourMinus = builder.get_object("btnHourMinus")
btnHourPlus = builder.get_object("btnHourPlus")

btnMinuteMinus = builder.get_object("btnMinuteMinus")
btnMinutePlus = builder.get_object("btnMinutePlus")

btnSecondMinus = builder.get_object("btnSecondMinus")
btnSecondPlus = builder.get_object("btnSecondPlus")

lblHours = builder.get_object("lblHours")
lblMinutes = builder.get_object("lblMinutes")
lblSeconds = builder.get_object("lblSeconds")

btnTimer = builder.get_object("btnStart")

"""
Connecting the buttons
"""
btnHourMinus.connect("clicked", decrement_hour)
btnHourPlus.connect("clicked", increment_hour)
btnMinuteMinus.connect("clicked", decrement_minute)
btnMinutePlus.connect("clicked", increment_minute)
btnSecondMinus.connect("clicked", decrement_second)
btnSecondPlus.connect("clicked", increment_second)
btnTimer.connect("clicked", timer)

"""
Showing the window
"""
window.show_all()

Gtk.main()
