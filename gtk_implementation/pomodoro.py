import gi, time, threading, subprocess, os, sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


"""
QoL stuff
"""


def switch_interfaces(status) -> None:
    if status == 0:
        lblTempoTrabalho.set_visible(False)
        lblTempoPausa.set_visible(False)
        lblMinutos.set_visible(False)
        lblMinutos2.set_visible(False)
        entryTrabalho.set_visible(False)
        entryPausa.set_visible(False)
        lblTempo.set_visible(True)
        lblTempo2.set_visible(True)
        lblRestante.set_visible(True)
        lblRestante2.set_visible(True)
    if status == 1:
        lblTempoTrabalho.set_visible(True)
        lblTempoPausa.set_visible(True)
        lblMinutos.set_visible(True)
        lblMinutos2.set_visible(True)
        entryTrabalho.set_visible(True)
        entryPausa.set_visible(True)
        lblTempo.set_visible(False)
        lblTempo2.set_visible(False)
        lblRestante.set_visible(False)
        lblRestante2.set_visible(False)


def hide_label() -> False:
    lblAviso.hide()
    return False


def show_label() -> None:
    lblAviso.set_visible(True)
    GLib.timeout_add_seconds(2, hide_label)


def validate_worktime(widget, event) -> None:
    text = entryTrabalho.get_text()

    if text.isnumeric():
        pass
    else:
        entryTrabalho.set_text("00")

    if text.isdigit():
        hour = int(text)
        if hour < 0:
            entryTrabalho.set_text("00")
    if len(text) == 1:
        entryTrabalho.set_text("0" + text)


def validate_pause_time(widget, event) -> None:
    text = entryPausa.get_text()

    if text.isnumeric():
        pass
    else:
        entryPausa.set_text("00")

    if text.isdigit():
        hour = int(text)
        if hour < 0:
            entryPausa.set_text("00")
    if len(text) == 1:
        entryPausa.set_text("0" + text)


"""
logical stuff
"""


def pomodoro(work_time, pause_time, pause_event, quit_event):
    work_time_seconds = work_time * 60
    pause_time_seconds = pause_time * 60
    lblRestante.set_text(str(work_time) + ":00")
    lblRestante2.set_text(str(pause_time) + ":00")

    if work_time == 0 or pause_time == 0:
        show_label()
        return False

    while True:
        if quit_event.is_set():
            print("Countdown Quit")
            btnPausa.set_sensitive(False)
            return

        print("Pomodoro Started")
        switch_interfaces(0)
        btnPausa.set_sensitive(True)
        print(f"Work for {work_time} minutes.")
        countdown(work_time_seconds, pause_event, quit_event, 0)

        if quit_event.is_set():
            print("Countdown Quit")
            btnPausa.set_sensitive(False)
            switch_interfaces(1)
            return

        subprocess.run(["notify-send", "Focuseer", "Pausa iniciada"])
        print("Work period ended.\n")
        lblRestante.set_text(str(work_time) + ":00")
        print(f"Pause for {pause_time} minutes.")
        countdown(pause_time_seconds, pause_event, quit_event, 1)

        if quit_event.is_set():
            print("Countdown Quit")
            btnPausa.set_sensitive(False)
            btnPomodoro.set_label("Iniciar")
            return

        subprocess.run(["notify-send", "Focuseer", "Fim da pausa"])
        print("Pause period ended.\n")
        lblRestante2.set_text(str(pause_time) + ":00")


"""
type = 0 -> work
type = 1 -> pause
"""


def countdown(seconds, pause_event, quit_event, type):
    while seconds > 0:
        if quit_event.is_set():
            return
        if not pause_event.is_set():
            mins, secs = divmod(seconds, 60)
            timer = f"{mins:02d}:{secs:02d}"
            if type == 0:
                lblRestante.set_text(timer)
            if type == 1:
                lblRestante2.set_text(timer)
            print(timer, end="\r")
            time.sleep(1)
            seconds -= 1
        else:
            time.sleep(1)
    if seconds == 0:
        timer = "00:00"
        print(timer, end="\r")
        print("\nfim")


def start_countdown(pause_event):
    global countdown_thread, seconds
    countdown_thread = threading.Thread(target=countdown, args=(seconds, pause_event))
    countdown_thread.start()


def pause_countdown(pause_event):
    pause_event.set()
    btnQuit.set_visible(True)
    btnResume.set_visible(True)


def resume_countdown(pause_event):
    global countdown_thread
    if countdown_thread and not countdown_thread.is_alive():
        countdown_thread = threading.Thread(
            target=countdown, args=(seconds, pause_event)
        )
        countdown_thread.start()
    pause_event.clear()
    btnQuit.set_visible(False)


def quit_countdown(pause_event, quit_event):
    quit_event.set()
    pause_event.set()
    btnQuit.set_visible(False)
    btnResume.set_visible(False)
    entryTrabalho.set_text("00")
    entryPausa.set_text("00")


def on_start_button_clicked(button, pause_event, entryTrabalho, entryPausa, quit_event):
    if countdown_thread and countdown_thread.is_alive():
        # The timer is still running, terminate it gracefully
        quit_countdown()
        countdown_thread.join()

    try:
        work_time_text = entryTrabalho.get_text()
        pause_time_text = entryPausa.get_text()
        work_time = int(work_time_text)
        pause_time = int(pause_time_text)

        quit_event.clear()
        pause_event.clear()

        threading.Thread(
            target=pomodoro, args=(work_time, pause_time, pause_event, quit_event)
        ).start()

    except ValueError:
        entryTrabalho.set_text("00")
        entryPausa.set_text("00")


def on_pause_button_clicked(button, pause_event):
    pause_countdown(pause_event)


def on_resume_button_clicked(button, pause_event):
    resume_countdown(pause_event)


def on_quit_button_clicked(button, pause_event, quit_event):
    quit_countdown(pause_event, quit_event)


countdown_thread = None
pause_event = threading.Event()
quit_event = threading.Event()


builder = Gtk.Builder()
builder.add_from_file("glade_screens/pomodoro_v2.glade")

window = builder.get_object("window")
window.set_title("Focuseer")

btnPomodoro = builder.get_object("btnPomodoro")
btnPausa = builder.get_object("btnPausa")
btnQuit = builder.get_object("btnQuit")
btnResume = builder.get_object("btnResume")
entryTrabalho = builder.get_object("entryTrabalho")
entryPausa = builder.get_object("entryPausa")


lblTempoTrabalho = builder.get_object("lblTempoTrabalho")
lblMinutos = builder.get_object("lblMinutos")
lblTempoPausa = builder.get_object("lblTempoPausa")
lblMinutos2 = builder.get_object("lblMinutos2")
lblTempo = builder.get_object("lblTempo")
lblTempo2 = builder.get_object("lblTempo2")
lblRestante = builder.get_object("lblRestante")
lblRestante2 = builder.get_object("lblRestante2")

btnPomodoro.connect(
    "clicked",
    on_start_button_clicked,
    pause_event,
    entryTrabalho,
    entryPausa,
    quit_event,
)


btnPausa.connect("clicked", on_pause_button_clicked, pause_event)
btnQuit.connect("clicked", on_quit_button_clicked, pause_event, quit_event)
btnResume.connect("clicked", on_resume_button_clicked, pause_event)
entryTrabalho.connect("focus-out-event", validate_worktime)
entryPausa.connect("focus-out-event", validate_pause_time)

""" nothing below this"""


lblAviso = builder.get_object("lblAviso")


css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)

window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnPomodoro.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnPausa.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
entryPausa.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

entryTrabalho.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window.show_all()
btnPausa.set_sensitive(False)
lblAviso.set_visible(False)
btnQuit.set_visible(False)

Gtk.main()
