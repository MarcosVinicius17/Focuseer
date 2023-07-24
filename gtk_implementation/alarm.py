import gi, datetime, subprocess, threading, time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from playsound import playsound


alarm_canceled = False


def switch_interfaces(status) -> None:
    if status == 0:
        btnAlarm.set_visible(False)
        btnHourPlus.set_visible(False)
        btnHourMinus.set_visible(False)
        btnMinuteMinus.set_visible(False)
        btnMinutePlus.set_visible(False)
        lblPonto.set_visible(False)
        entryHours.set_visible(False)
        entryMinutes.set_visible(False)
        chkAlarm.set_visible(False)
        btnCancelar.set_visible(True)
        lblMensagem.set_visible(True)
        lblTempo.set_visible(True)
    if status == 1:
        btnAlarm.set_visible(True)
        btnHourPlus.set_visible(True)
        btnHourMinus.set_visible(True)
        btnMinuteMinus.set_visible(True)
        btnMinutePlus.set_visible(True)
        lblPonto.set_visible(True)
        entryHours.set_visible(True)
        entryMinutes.set_visible(True)
        chkAlarm.set_visible(True)
        btnCancelar.set_visible(False)
        lblMensagem.set_visible(False)
        lblTempo.set_visible(False)


def increment_hour(button) -> None:
    try:
        current_hour = int(entryHours.get_text())
        current_hour += 1
        if current_hour >= 24:
            current_hour = "00"
        entryHours.set_text(str(current_hour))
        validate_hour(entryHours, "focus-out-event")
    except ValueError:
        entryHours.set_text("00")


def decrement_hour(button) -> None:
    try:
        current_hour = int(entryHours.get_text())
        current_hour -= 1
        if current_hour == -1:
            current_hour = "23"
        entryHours.set_text(str(current_hour))
        validate_hour(entryHours, "focus-out-event")
    except ValueError:
        entryHours.set_text("00")


def increment_minute(button) -> None:
    try:
        current_minute = int(entryMinutes.get_text())
        current_minute += 1
        if current_minute == 60:
            current_minute = "00"
        entryMinutes.set_text(str(current_minute))
        validate_minute(entryMinutes, "focus-out-event")
    except ValueError:
        entryMinutes.set_text("00")


def decrement_minute(button) -> None:
    try:
        current_minute = int(entryMinutes.get_text())
        current_minute -= 1
        if current_minute == -1:
            current_minute = "59"
        entryMinutes.set_text(str(current_minute))
        validate_minute(entryMinutes, "focus-out-event")
    except ValueError:
        entryMinutes.set_text("00")


def validate_hour(widget, event):
    text = entryHours.get_text()

    if text.isnumeric():
        pass
    else:
        entryHours.set_text("23")

    if text.isdigit():
        hour = int(text)
        if hour < 0 or hour > 23:
            entryHours.set_text("23")
    if len(text) == 1:
        entryHours.set_text("0" + text)


def validate_minute(widget, event) -> None:
    text = entryMinutes.get_text()
    if text.isnumeric():
        pass
    else:
        entryMinutes.set_text("59")

    if text.isdigit():
        minute = int(text)
        if minute < 0 or minute > 59:
            entryMinutes.set_text("59")
    if len(text) == 1:
        entryMinutes.set_text("0" + text)


def start_alarm(button) -> None:
    thread = threading.Thread(target=alarm)
    thread.start()


def alarm() -> None:
    global alarm_canceled
    runs = 0

    alarm_time = "00:00"
    alarm_hour = entryHours.get_text()
    alarm_minute = entryMinutes.get_text()

    alarm_time = alarm_hour + ":" + alarm_minute
    alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M")
    print(f"Alarm set for {alarm_time}")
    lblTempo.set_text(str(alarm_hour + ":" + alarm_minute))
    switch_interfaces(0)

    while not alarm_canceled:
        current_time = datetime.datetime.now()
        if current_time.strftime("%H:%M") == alarm_time.strftime("%H:%M"):
            if runs < 1:
                if chkAlarm.get_active():
                    switch_interfaces(1)
                    subprocess.run(["notify-send", "Focuseer", "Seu alarme"])
                    runs += 1
                else:
                    switch_interfaces(1)
                    subprocess.run(["notify-send", "Focuseer", "Seu alarme"])
                    mp3_file = (
                        "/home/marcos/Desktop/UNIP/tcc/nao_programacao/sounds/alarm.mp3"
                    )
                    playsound(mp3_file)
                    runs += 1
            if runs == 1:
                break

        # adiciona um delay de 30 segundos para verificar a hora
        time.sleep(30)
    alarm_canceled = False


def cancel_alarm(button) -> None:
    global alarm_canceled
    alarm_canceled = True
    print("alarme cancelado")
    switch_interfaces(1)


builder = Gtk.Builder()
builder.add_from_file("glade_screens/alarm.glade")

window = builder.get_object("Window")


btnAlarm = builder.get_object("btnAlarm")
btnAlarm.connect("clicked", start_alarm)
btnCancelar = builder.get_object("btnCancelar")
btnCancelar.connect("clicked", cancel_alarm)

btnHourMinus = builder.get_object("btnHoursMinus")
btnHourPlus = builder.get_object("btnHoursPlus")

btnMinuteMinus = builder.get_object("btnMinuteMinus")
btnMinutePlus = builder.get_object("btnMinutePlus")

entryHours = builder.get_object("hours")
entryMinutes = builder.get_object("minutes")
lblPonto = builder.get_object("lblPonto")


# Instead of "changed" effect, the entries are validated after the user leave the focus
entryHours.connect("focus-out-event", validate_hour)
entryMinutes.connect("focus-out-event", validate_minute)

chkAlarm = builder.get_object("chkAlarm")

lblMensagem = builder.get_object("lblMensagem")
lblTempo = builder.get_object("lblTempo")


btnHourMinus.connect("clicked", decrement_hour)
btnHourPlus.connect("clicked", increment_hour)
btnMinuteMinus.connect("clicked", decrement_minute)
btnMinutePlus.connect("clicked", increment_minute)

# CSS
css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)

window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnHourPlus.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnHourMinus.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnMinutePlus.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnMinuteMinus.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
entryHours.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
entryMinutes.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


window.show_all()
lblMensagem.set_visible(False)
lblTempo.set_visible(False)
btnCancelar.set_visible(False)
Gtk.main()
