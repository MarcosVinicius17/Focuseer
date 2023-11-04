import gi, subprocess, sys, datetime, locale, re, json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk

# Traduz o texto do subtitulo da headerbar
locale.setlocale(locale.LC_ALL, "pt_BR.utf8")


def set_hora_encerramento(hora) -> None:
    with open("gtk_implementation/reports/data.json", "r") as file:
        data = json.load(file)
    data["hora_encerramento"]["hora"] = hora

    with open("gtk_implementation/reports/data.json", "w") as file:
        json.dump(data, file, indent=4)


def set_headerbar_title(username):
    headerbar.set_title(username)
    window.show_all()


def logout(menu_item):
    subprocess.Popen([sys.executable, "gtk_implementation/login.py"])
    window.destroy()


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
        "nao_programacao/logos/logo_login_white.png"
    )

    about_dialog.set_logo(logo_pixbuf)

    # Aplica CSS ao dialog
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path("gtk_implementation/custom_colors.css")
    screen = Gdk.Screen.get_default()
    style_context = Gtk.StyleContext()
    style_context.add_provider_for_screen(
        screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
    )

    about_dialog.run()
    about_dialog.destroy()


def validate_time_format(input_string):
    # regex para o formato HH:MM
    pattern = r"^[0-9]{2}:[0-9]{2}$"

    # verifica se a entrada o usuario eh compativel com o regex
    if re.match(pattern, input_string):
        # separa horas de minutos
        hours, minutes = input_string.split(":")

        # verifica se eh um horario valido
        if 0 <= int(hours) <= 23 and 0 <= int(minutes) <= 59:
            return True
    return False


def start_work(button):
    dialog = Gtk.Dialog(
        title="Horário de encerramento",
        buttons=(
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,
        ),
    )
    dialog.set_default_size(200, 50)

    # Create a text entry field
    entry = Gtk.Entry()
    entry.set_text("Hora de encerramento:")
    entry.set_activates_default(True)
    dialog.vbox.pack_start(entry, True, True, 0)
    entry.show()

    # Run the dialog and get the response
    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        is_entry_valid = validate_time_format(entry.get_text())
        if is_entry_valid:
            set_hora_encerramento(entry.get_text())
            subprocess.Popen([sys.executable, "gtk_implementation/workscreen.py"])

        else:
            dialog.destroy()
            warning_dialog = Gtk.MessageDialog(
                parent=None,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Horário inválido. Utilize o formato HH:MM",
            )
            warning_dialog.run()
            warning_dialog.destroy()
    dialog.destroy()


def open_alarm(button):
    subprocess.Popen([sys.executable, "gtk_implementation/alarm.py"])


def open_stopwatch(button):
    subprocess.Popen([sys.executable, "gtk_implementation/stopwatch.py"])


def open_timer(buton):
    subprocess.Popen([sys.executable, "gtk_implementation/timer.py"])


def open_pomodoro(button):
    subprocess.Popen([sys.executable, "gtk_implementation/pomodoro.py"])


def open_process_monitor(button):
    subprocess.Popen([sys.executable, "gtk_implementation/monitor.py"])


def open_trello(button):
    subprocess.Popen([sys.executable, "gtk_implementation/trello_start.py"])


def open_notes(button):
    subprocess.Popen([sys.executable, "gtk_implementation/notes_start.py"])


def open_calendar(button):
    subprocess.Popen([sys.executable, "gtk_implementation/calendar.py"])


def open_settings(button):
    print("settings")


def open_reports(button):
    print("reports")


def open_stats(button):
    print("Stats")


def show_hide_window(button, window_to_toggle):
    if window_to_toggle.get_property("visible"):
        window_to_toggle.hide()
    else:
        window_to_toggle.show()


builder = Gtk.Builder()
builder.add_from_file("glade_screens/homepage.glade")

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
headerbar.set_title("username")


menuButton = builder.get_object("menuButton")

menuButton.set_label("●●●")


menuAbout = builder.get_object("about")
menuLogout = builder.get_object("logout")


menuAbout.connect("activate", open_about)
menuLogout.connect("activate", logout)

css_provider = Gtk.CssProvider()

css_provider.load_from_path("gtk_implementation/custom_colors.css")


window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnAlarm.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnTimer.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnNotes.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnTrello.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnPomodoro.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnSettings.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnStats.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnReports.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnStart.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnMonitor.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
headerbar.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

btnCalendar.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
menuButton.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


# window.show_all()
# Gtk.main()
