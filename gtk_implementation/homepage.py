import gi, subprocess, sys, datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk


css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)


def modo_noturno(menu_item):
    print("modo noturno")


def logout(menu_item):
    print("logout")


def open_about(button):
    about_dialog = Gtk.AboutDialog()
    about_dialog.set_program_name("Focuseer")
    about_dialog.set_name("about_dialog")
    about_dialog.set_version("1.0")
    about_dialog.set_comments("Mantenha a produtividade ao trabalhar de forma remota")
    about_dialog.set_website("https://github.com/MarcosVinicius17/Focuseer")
    about_dialog.set_website_label("Github")
    about_dialog.set_authors(["Marcos Vinícius F. Vieira"])

    logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file(
        "/home/marcos/Desktop/UNIP/tcc/nao_programacao/logos/logo_login_white.png"
    )

    about_dialog.set_logo(logo_pixbuf)

    # Aplica CSS ao dialog

    screen = Gdk.Screen.get_default()
    style_context = Gtk.StyleContext()
    style_context.add_provider_for_screen(
        screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
    )

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


def open_pomodoro(button):
    # subprocess.Popen([sys.executable, "pomodoro.py"])
    print("pomodoro")


def open_process_monitor(button):
    # subprocess.Popen([sys.executable, "process_monitor.py"])
    print("monitor")


def open_trello(button):
    # subprocess.Popen([sys.executable, "trello.py"])
    print("trello")


def open_notes(button):
    subprocess.Popen([sys.executable, "gtk_implementation/notes_start.py"])


def open_calendar(button):
    subprocess.Popen([sys.executable, "gtk_implementation/calendar.py"])


def open_settings(button):
    print("settings")


def open_reports(button):
    print("reports")


def open_stats(button):
    print("stats")


builder = Gtk.Builder()
builder.add_from_file("glade_screens/homepage_menubutton.glade")

window = builder.get_object("Window")


btnAlarm = builder.get_object("btnAlarm")
btnAlarm.connect("clicked", open_alarm)

btnTimer = builder.get_object("btnTimer")
btnTimer.connect("clicked", open_timer)


btnNotes = builder.get_object("btnNotes")
btnNotes.connect("clicked", open_notes)

btnMonitor = builder.get_object("btnMonitor")
btnMonitor.connect("clicked", open_process_monitor)

btnTrello = builder.get_object("btnTrello")
btnTrello.connect("clicked", open_trello)

btnPomodoro = builder.get_object("btnPomodoro")
btnPomodoro.connect("clicked", open_pomodoro)

btnSettings = builder.get_object("btnSettings")
btnSettings.connect("clicked", open_settings)

btnReports = builder.get_object("btnReports")
btnReports.connect("clicked", open_reports)

btnStats = builder.get_object("btnStats")
btnStats.connect("clicked", open_stats)

btnCalendar = builder.get_object("btnCalendar")
btnCalendar.connect("clicked", open_calendar)

btnStart = builder.get_object("btnStart")
btnStart.connect("clicked", start_work)


lblDate = builder.get_object("lblCurrentDate")
now = datetime.datetime.now()
day = now.day
month = now.strftime("%B")
hour = now.hour
minute = now.minute

# headerbar
headerbar = builder.get_object("headerBar")
headerbar.set_subtitle(f"{day:02.0f} de {month}, {hour:02.0f}:{minute:02.0f}")
headerbar.set_title("Marcos Vinícius F. Vieira")

# menubutton
menuButton = builder.get_object("menuButton")

# menuButton.set_label("Settings")
# its just works
menuButton.set_label("●●●")

menuModoNoturno = builder.get_object("modoNoturno")
menuAbout = builder.get_object("about")
menuLogout = builder.get_object("logout")

menuModoNoturno.connect("activate", modo_noturno)
menuAbout.connect("activate", open_about)
menuLogout.connect("activate", logout)


context_window = window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnAlarm = btnAlarm.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnTimer = btnTimer.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnNotes = btnNotes.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnTrello = btnTrello.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnPomodoro = btnPomodoro.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnSettings = btnSettings.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
cotnext_btnStats = btnStats.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnReports = btnReports.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnStart = btnStart.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnMonitor = btnMonitor.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_headerbar = headerbar.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

context_calendar = btnCalendar.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


window.show_all()
Gtk.main()
