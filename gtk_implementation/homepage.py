import gi, subprocess, sys, datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf


"""
Para o notes.glade, verificar os widgets GtkNotebook e GtkTreeView
"""


def open_about(button):
    about_dialog = Gtk.AboutDialog()
    try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            "/home/marcos/Desktop/UNIP/tcc/nao_programacao/logos/logo_icone.png"
        )
    except:
        print("erro")

    # Set properties for the about dialog
    about_dialog.set_program_name("Focuseer")
    about_dialog.set_version("1.0")
    about_dialog.set_comments("Keep your productivity while working remotely")
    about_dialog.set_website("https://www.example.com")
    about_dialog.set_authors(["Marcos Vinícius"])

    about_dialog.set_icon(pixbuf)
    about_dialog.set_logo_icon_name("my-application-icon")
    about_dialog.set_transient_for(button.get_toplevel())

    # Run the dialog
    about_dialog.run()
    about_dialog.destroy()


def start_work(button):
    print("ok")


def open_alarm(button):
    subprocess.Popen([sys.executable, "gtk_implementation/alarm.py"])


def open_stopwatch(button):
    subprocess.Popen([sys.executable, "gtk_implementation/stopwatch.py"])


def open_timer(buton):
    subprocess.Popen([sys.executable, "gtk_implementation/timer.py"])


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


btnAbout = builder.get_object("btnAbout")
btnAbout.connect("clicked", open_about)

btnStart = builder.get_object("btnStart")
btnStart.connect("clicked", start_work)

lblDate = builder.get_object("lblCurrentDate")
now = datetime.datetime.now()
day = now.day
month = now.strftime("%B")
hour = now.hour
minute = now.minute

lblDate.set_text(f"{day:02.0f} de {month}, {hour:02.0f}:{minute:02.0f}")


css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)

context_window = window.get_style_context()
context_btnAbout = btnAbout.get_style_context()
context_btnAlarm = btnAlarm.get_style_context()
context_btnTimer = btnTimer.get_style_context()
context_btnStopwatch = btnStopwatch.get_style_context()
context_btnNotes = btnNotes.get_style_context()
context_btnStart = btnStart.get_style_context()


context_window.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
context_btnAbout.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
context_btnAlarm.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
context_btnTimer.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
context_btnStopwatch.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
context_btnNotes.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


window.show_all()

Gtk.main()
