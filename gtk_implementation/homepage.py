import gi, subprocess, sys, datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


"""
Depois de fazer a GUI com o Glade, suas funcionalidades sao implantadas deste jeito.
Deve-se carregar o arquivo .glade e entao ir modificando-o.
"""

"""
Para o notes.glade, verificar os widgets GtkNotebook e GtkTreeView
"""


"""
Opens alarm.py
"""


def open_alarm(button):
    subprocess.Popen([sys.executable, "gtk_implementation/alarm.py"])


def open_stopwatch(button):
    subprocess.Popen([sys.executable, "gtk_implementation/stopwatch.py"])


def open_timer(buton):
    subprocess.Popen([sys.executable, "gtk_implementation/timer.py"])


"""Not created yet"""


"""def open_pomodoro(button):
    subprocess.Popen([sys.executable, "pomodoro.py"])


def open_site_monitor(button):
    subprocess.Popen([sys.executable, "site_monitor.py"])


def open_process_monitor(button):
    subprocess.Popen([sys.executable, "process_monitor.py"])


def open_profile(button):
    subprocess.Popen([sys.executable, "profile.py"])
"""


def open_notes(button):
    subprocess.Popen([sys.executable, "write_note.py"])


builder = Gtk.Builder()
builder.add_from_file("glade_screens/homepage.glade")

window = builder.get_object("Window")


btnAlarm = builder.get_object("btnAlarm")
btnAlarm.connect("clicked", open_alarm)

btnStopwatch = builder.get_object("btnStopwatch")
btnStopwatch.connect("clicked", open_stopwatch)

btnTimer = builder.get_object("btnTimer")
btnTimer.connect("clicked", open_timer)


btnNotes = builder.get_object("btnNotes")
btnNotes.connect("clicked", open_notes)


lblDate = builder.get_object("lblCurrentDate")
now = datetime.datetime.now()
day = now.day
month = now.strftime("%B")
hour = now.hour
minute = now.minute

lblDate.set_text(f"{day:02.0f} de {month}, {hour:02.0f}:{minute:02.0f}")


"""
Exibir a janela
"""

window.show_all()

Gtk.main()
