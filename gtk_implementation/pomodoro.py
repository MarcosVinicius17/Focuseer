import gi, time, threading, subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


def hide_label() -> False:
    lblAviso.hide()
    return False


def show_label() -> None:
    lblAviso.set_visible(True)
    GLib.timeout_add_seconds(2, hide_label)


def pause(button) -> None:
    print("pausad")
    btnPausa.set_label("Cancelar")
    btnPausa.connect("clicked", stop_pomodoro)


def stop_pomodoro(button) -> None:
    print("the end")


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


def pomodoro(work_time, pause_time) -> None:
    work_time_seconds = work_time * 60
    pause_time_seconds = pause_time * 60

    if work_time == 0 or pause_time == 0:
        show_label()
        return False

    while True:
        print("Pomodoro Started")
        btnPausa.set_sensitive(True)
        print(f"Work for {work_time} minutes.")
        countdown(work_time_seconds)
        subprocess.run(["notify-send", "Focuseer", "Pausa iniciada"])
        print("Work period ended.\n")

        print(f"Pause for {pause_time} minutes.")
        countdown(pause_time_seconds)
        print("Pause period ended.\n")
        subprocess.run(["notify-send", "Focuseer", "Fim da pausa"])


def countdown(seconds) -> None:
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1


def start_pomodoro() -> None:
    work_time = int(entryTrabalho.get_text())
    pause_time = int(entryPausa.get_text())
    threading.Thread(target=pomodoro, args=(work_time, pause_time)).start()


def on_button_clicked(button) -> None:
    start_pomodoro()


builder = Gtk.Builder()
builder.add_from_file("glade_screens/pomodoro_v2.glade")

window = builder.get_object("window")
window.set_title("Focuseer")

btnPomodoro = builder.get_object("btnPomodoro")
btnPomodoro.connect("clicked", on_button_clicked)

btnPausa = builder.get_object("btnPausa")
btnPausa.connect("clicked", pause)


entryTrabalho = builder.get_object("entryTrabalho")
entryPausa = builder.get_object("entryPausa")
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
Gtk.main()
