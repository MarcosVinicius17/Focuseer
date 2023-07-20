import gi, time, threading, subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


"""
QoL stuff
"""


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

    if work_time == 0 or pause_time == 0:
        show_label()
        return False

    while True:
        if quit_event.is_set():
            print("Countdown Quit")
            btnPausa.set_sensitive(False)
            return

        print("Pomodoro Started")
        btnPausa.set_sensitive(True)
        print(f"Work for {work_time} minutes.")
        countdown(work_time_seconds, pause_event, quit_event)

        if quit_event.is_set():
            print("Countdown Quit")
            btnPausa.set_sensitive(False)
            return

        subprocess.run(["notify-send", "Focuseer", "Pausa iniciada"])
        print("Work period ended.\n")

        print(f"Pause for {pause_time} minutes.")
        countdown(pause_time_seconds, pause_event, quit_event)

        if quit_event.is_set():
            print("Countdown Quit")
            btnPausa.set_sensitive(False)
            btnPomodoro.set_label("Iniciar")
            return

        subprocess.run(["notify-send", "Focuseer", "Fim da pausa"])
        print("Pause period ended.\n")


def countdown(seconds, pause_event, quit_event):
    while seconds > 0:
        if quit_event.is_set():
            return
        if not pause_event.is_set():
            mins, secs = divmod(seconds, 60)
            timer = f"{mins:02d}:{secs:02d}"
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


"""
not 100% about this...but it works for now
"""


def pause_countdown(pause_event):
    if not pause_countdown.disconnected:
        btnPomodoro.set_label("Continuar")

        btnPomodoro.disconnect(start_id)
        pause_countdown.disconnected = True

        resume_id = btnPomodoro.connect(
            "clicked", on_resume_button_clicked, pause_event
        )
        # btnQuit.set_visible(True)
    pause_event.set()
    btnQuit.set_visible(True)


pause_countdown.disconnected = False


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
    btnPomodoro.set_label("Iniciar")
    """arrumar esta parte"""
    # btnPomodoro.disconnect(resume_id)


def on_start_button_clicked(button, pause_event, entryTrabalho, entryPausa, quit_event):
    try:
        work_time_text = entryTrabalho.get_text()
        pause_time_text = entryPausa.get_text()
        work_time = int(work_time_text)
        pause_time = int(pause_time_text)
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
entryTrabalho = builder.get_object("entryTrabalho")
entryPausa = builder.get_object("entryPausa")

start_id = btnPomodoro.connect(
    "clicked",
    on_start_button_clicked,
    pause_event,
    entryTrabalho,
    entryPausa,
    quit_event,
)


btnPausa.connect("clicked", on_pause_button_clicked, pause_event)
btnQuit.connect("clicked", on_quit_button_clicked, pause_event, quit_event)
entryTrabalho.connect("focus-out-event", validate_worktime)
entryPausa.connect("focus-out-event", validate_pause_time)


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
