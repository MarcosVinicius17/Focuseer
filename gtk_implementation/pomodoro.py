import gi, time, threading, subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def pause(button):
    print("pausad")


def pomodoro(work_time, pause_time):
    work_time_seconds = work_time * 60
    pause_time_seconds = pause_time * 60
    print("Pomodoro Started!")

    while True:
        print(f"Work for {work_time} minutes.")
        countdown(work_time_seconds)
        subprocess.run(["notify-send", "Focuseer", "Pausa iniciada"])
        print("Work period ended.\n")

        print(f"Pause for {pause_time} minutes.")
        countdown(pause_time_seconds)
        print("Pause period ended.\n")
        subprocess.run(["notify-send", "Focuseer", "Fim da pausa"])


def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1


def start_pomodoro():
    work_time = int(entryTrabalho.get_text())
    pause_time = int(entryPausa.get_text())
    threading.Thread(target=pomodoro, args=(work_time, pause_time)).start()


def on_button_clicked(button):
    # RESOLVER O PROBLEMA DO BOTAO
    btnPausa.set_sensitive(True)
    start_pomodoro()


builder = Gtk.Builder()
builder.add_from_file("glade_screens/pomodoro_v2.glade")

window = builder.get_object("window")

btnPomodoro = builder.get_object("btnPomodoro")
btnPomodoro.connect("clicked", on_button_clicked)

btnPausa = builder.get_object("btnPausa")
btnPausa.connect("clicked", pause)


# btnPausa.set_visible(False)

entryTrabalho = builder.get_object("entryTrabalho")
entryPausa = builder.get_object("entryPausa")


css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)

context_window = window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnPomodoro = btnPomodoro.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnPausa = btnPausa.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_entryPausa = entryPausa.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

context_entryTrabalho = entryTrabalho.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


window.show_all()


Gtk.main()
