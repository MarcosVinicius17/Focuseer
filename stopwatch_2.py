import gi, time, threading

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

"""
Obter o texto das 3 labels -> incrementar segundos. Ao chegar em 60, resetar e incrementar os minutos. Repetir para as horas
"""

is_stopwatch_running = True


def cronometro(button) -> None:
    thread = threading.Thread(target=incrementar)
    thread.start()


def stop(button) -> None:
    global is_stopwatch_running
    is_stopwatch_running = False
    print("Parado")
    btnStop.set_label("Resume")


def incrementar() -> None:

    current_seconds = int(seconds.get_text())
    current_minutes = int(minutes.get_text())
    current_hours = int(hours.get_text())

    while is_stopwatch_running:
        current_seconds += 1
        time.sleep(1)

        if current_seconds == 60:
            current_seconds = 0
            current_minutes += 1
        if current_minutes == 60:
            current_minutes = 0
            current_hours += 1
        print(f"{current_hours}:{current_minutes}:{current_seconds}")
        seconds.set_text(str(current_seconds))


builder = Gtk.Builder()
builder.add_from_file("stopwatch.glade")

window = builder.get_object("Window")
"""
Obtendo as labels usadas no cronometro
"""
hours = builder.get_object("lblHours")
minutes = builder.get_object("lblMinutes")
seconds = builder.get_object("lblSeconds")


btnStart = builder.get_object("btnStart")
btnStart.connect("clicked", cronometro)
btnStop = builder.get_object("btnStop")
btnStop.connect("clicked", stop)

window.show_all()

Gtk.main()
