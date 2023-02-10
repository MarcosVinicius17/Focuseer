import gi, subprocess, sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


"""
Depois de fazer a GUI com o Glade, suas funcionalidades sao implantadas deste jeito.
Deve-se carregar o arquivo .glade e entao ir modificando-o.
"""

"""
Opens alarm.py
"""


def open_alarm(button):
    subprocess.Popen([sys.executable, "alarm.py"])


def open_stopwatch(button):
    subprocess.Popen([sys.executable, "stopwatch.py"])


def open_timer(buton):
    subprocess.Popen([sys.executable, "timer.py"])


"""Not created yet"""


"""def open_pomodoro(button):
    subprocess.Popen([sys.executable, "pomodoro.py"])


def open_site_monitor(button):
    subprocess.Popen([sys.executable, "site_monitor.py"])


def open_process_monitor(button):
    subprocess.Popen([sys.executable, "process_monitor.py"])


def open_profile(button):
    subprocess.Popen([sys.executable, "profile.py"])

def open_notes(button):
    subprocess.Popen([sys.executable, "notes.py"])"""


builder = Gtk.Builder()
builder.add_from_file("homepage.glade")

window = builder.get_object("Window")


btnAlarm = builder.get_object("btnAlarm")
btnAlarm.connect("clicked", open_alarm)


"""
Exibir a janela
"""

window.show_all()

Gtk.main()
