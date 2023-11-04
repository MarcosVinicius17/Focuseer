import gi, datetime, subprocess, threading, time, json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from playsound import playsound


def update_alarm_info(active, ring_time):
    with open("gtk_implementation/reports/data.json", "r") as file:
        data = json.load(file)

    data["alarm_info"]["active"] = active
    data["alarm_info"]["ring_time"] = ring_time

    with open("gtk_implementation/reports/data.json", "w") as file:
        json.dump(data, file, indent=4)


def on_delete_event(widget, event):
    widget.hide()
    print("escondendo janela")
    return True


class Alarm:
    def __init__(self):
        self.alarm_canceled = False

        self.builder = Gtk.Builder()
        self.builder.add_from_file("glade_screens/alarm.glade")
        self.window = self.builder.get_object("Window")
        self.window.connect("delete-event", on_delete_event)

        self.btnAlarm = self.builder.get_object("btnAlarm")
        self.btnAlarm.connect("clicked", self.start_alarm)
        self.btnCancelar = self.builder.get_object("btnCancelar")
        self.btnCancelar.connect("clicked", self.cancel_alarm)

        self.btnHourMinus = self.builder.get_object("btnHoursMinus")
        self.btnHourPlus = self.builder.get_object("btnHoursPlus")
        self.btnMinuteMinus = self.builder.get_object("btnMinuteMinus")
        self.btnMinutePlus = self.builder.get_object("btnMinutePlus")

        self.btnHourMinus.connect("clicked", self.decrement_hour)
        self.btnHourPlus.connect("clicked", self.increment_hour)
        self.btnMinuteMinus.connect("clicked", self.decrement_minute)
        self.btnMinutePlus.connect("clicked", self.increment_minute)

        self.entryHours = self.builder.get_object("hours")
        self.entryMinutes = self.builder.get_object("minutes")
        self.lblPonto = self.builder.get_object("lblPonto")

        self.entryHours.connect("focus-out-event", self.validate_hour)
        self.entryMinutes.connect("focus-out-event", self.validate_minute)

        self.chkAlarm = self.builder.get_object("chkAlarm")
        self.lblMensagem = self.builder.get_object("lblMensagem")
        self.lblTempo = self.builder.get_object("lblTempo")

        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path("gtk_implementation/custom_colors.css")

        self.window.get_style_context().add_provider(
            self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.btnHourPlus.get_style_context().add_provider(
            self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.btnHourMinus.get_style_context().add_provider(
            self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.btnMinutePlus.get_style_context().add_provider(
            self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.btnMinuteMinus.get_style_context().add_provider(
            self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.entryHours.get_style_context().add_provider(
            self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.entryMinutes.get_style_context().add_provider(
            self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.alarm_canceled = False

    def switch_interfaces(self, status):
        if status == 0:
            self.btnAlarm.set_visible(False)
            self.btnHourPlus.set_visible(False)
            self.btnHourMinus.set_visible(False)
            self.btnMinuteMinus.set_visible(False)
            self.btnMinutePlus.set_visible(False)
            self.lblPonto.set_visible(False)
            self.entryHours.set_visible(False)
            self.entryMinutes.set_visible(False)
            self.chkAlarm.set_visible(False)
            self.btnCancelar.set_visible(True)
            self.lblMensagem.set_visible(True)
            self.lblTempo.set_visible(True)
        if status == 1:
            self.btnAlarm.set_visible(True)
            self.btnHourPlus.set_visible(True)
            self.btnHourMinus.set_visible(True)
            self.btnMinuteMinus.set_visible(True)
            self.btnMinutePlus.set_visible(True)
            self.lblPonto.set_visible(True)
            self.entryHours.set_visible(True)
            self.entryMinutes.set_visible(True)
            self.chkAlarm.set_visible(True)
            self.btnCancelar.set_visible(False)
            self.lblMensagem.set_visible(False)
            self.lblTempo.set_visible(False)

    def increment_hour(self, button):
        try:
            current_hour = int(self.entryHours.get_text())
            current_hour += 1
            if current_hour >= 24:
                current_hour = "00"
            self.entryHours.set_text(str(current_hour))
            self.validate_hour(self.entryHours, "focus-out-event")
        except ValueError:
            self.entryHours.set_text("00")

    def decrement_hour(self, button):
        try:
            current_hour = int(self.entryHours.get_text())
            current_hour -= 1
            if current_hour == -1:
                current_hour = "23"
            self.entryHours.set_text(str(current_hour))
            self.validate_hour(self.entryHours, "focus-out-event")
        except ValueError:
            self.entryHours.set_text("00")

    def increment_minute(self, button):
        try:
            current_minute = int(self.entryMinutes.get_text())
            current_minute += 1
            if current_minute == 60:
                current_minute = "00"
            self.entryMinutes.set_text(str(current_minute))
            self.validate_minute(self.entryMinutes, "focus-out-event")
        except ValueError:
            self.entryMinutes.set_text("00")

    def decrement_minute(self, button):
        try:
            current_minute = int(self.entryMinutes.get_text())
            current_minute -= 1
            if current_minute == -1:
                current_minute = "59"
            self.entryMinutes.set_text(str(current_minute))
            self.validate_minute(self.entryMinutes, "focus-out-event")
        except ValueError:
            self.entryMinutes.set_text("00")

    def validate_hour(self, widget, event):
        text = self.entryHours.get_text()

        if text.isnumeric():
            pass
        else:
            self.entryHours.set_text("23")

        if text.isdigit():
            hour = int(text)
            if hour < 0 or hour > 23:
                self.entryHours.set_text("23")
        if len(text) == 1:
            self.entryHours.set_text("0" + text)

    def validate_minute(self, widget, event):
        text = self.entryMinutes.get_text()
        if text.isnumeric():
            pass
        else:
            self.entryMinutes.set_text("59")

        if text.isdigit():
            minute = int(text)
            if minute < 0 or minute > 59:
                self.entryMinutes.set_text("59")
        if len(text) == 1:
            self.entryMinutes.set_text("0" + text)

    def start_alarm(self, button):
        thread = threading.Thread(target=self.alarm)
        thread.start()

    def alarm(self):
        global alarm_canceled
        runs = 0

        alarm_time = "00:00"
        alarm_hour = self.entryHours.get_text()
        alarm_minute = self.entryMinutes.get_text()

        alarm_time = alarm_hour + ":" + alarm_minute
        alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M")
        print(f"Alarm set for {alarm_time}")
        self.lblTempo.set_text(str(alarm_hour + ":" + alarm_minute))
        self.switch_interfaces(0)

        """
        atualiza a estrutura contendo informacoes para a workscreen
        """

        update_alarm_info(True, str(alarm_hour + ":" + alarm_minute))

        while not self.alarm_canceled:
            current_time = datetime.datetime.now()
            if current_time.strftime("%H:%M") == alarm_time.strftime("%H:%M"):
                if runs < 1:
                    if self.chkAlarm.get_active():
                        self.switch_interfaces(1)
                        subprocess.run(["notify-send", "Focuseer", "Seu alarme"])
                        runs += 1
                    else:
                        self.switch_interfaces(1)
                        subprocess.run(["notify-send", "Focuseer", "Seu alarme"])
                        mp3_file = "/home/marcos/Desktop/UNIP/tcc/nao_programacao/sounds/alarm.mp3"
                        playsound(mp3_file)
                        runs += 1
                if runs == 1:
                    break

            # adiciona um delay de 30 segundos para verificar a hora
            time.sleep(30)
        self.alarm_canceled = False

    def cancel_alarm(self, button):
        global alarm_canceled
        self.alarm_canceled = True
        print("alarme cancelado")
        self.switch_interfaces(1)
        update_alarm_info(False, None)

    def run(self):
        self.window.show_all()
        self.lblMensagem.set_visible(False)
        self.lblTempo.set_visible(False)
        self.btnCancelar.set_visible(False)
        Gtk.main()


if __name__ == "__main__":
    app = Alarm()
    app.run()
