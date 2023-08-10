import gi, time, subprocess, threading, json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from playsound import playsound
from datetime import datetime, timedelta


"""
bug grave quando se executa o timer.
"""


# calcula que horas o timer ira tocar
def get_timer_end(add_hour, add_minute, add_second) -> str:
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute

    current_time = datetime.now().replace(
        hour=current_hour, minute=current_minute, second=0, microsecond=0
    )
    time_to_add = timedelta(hours=add_hour, minutes=add_minute, seconds=add_second)
    new_time = current_time + time_to_add
    print("timer ira acabar em ", new_time.strftime("%H:%M:%S"))
    return new_time.strftime("%H:%M:%S")


def update_timer_info(active, timer_end) -> None:
    with open("gtk_implementation/temp_data.json", "r") as file:
        data = json.load(file)

    data["timer_info"]["active_timer"] = active
    data["timer_info"]["timer_end"] = timer_end

    with open("gtk_implementation/temp_data.json", "w") as file:
        json.dump(data, file, indent=4)


class TimerApp:
    def __init__(self):
        self.pause_event = threading.Event()
        self.quit_event = threading.Event()
        self.timer_thread = None  # Store the currently running timer thread

        builder = Gtk.Builder()
        builder.add_from_file("glade_screens/timer.glade")

        self.window = builder.get_object("Window")
        self.entryHours = builder.get_object("hours")
        self.entryMinutes = builder.get_object("minutes")
        self.entrySeconds = builder.get_object("seconds")

        self.hours_inc_btn = builder.get_object("btnHourPlus")
        self.hours_dec_btn = builder.get_object("btnHourMinus")
        self.minutes_inc_btn = builder.get_object("btnMinutePlus")
        self.minutes_dec_btn = builder.get_object("btnMinuteMinus")
        self.seconds_inc_btn = builder.get_object("btnSecondPlus")
        self.seconds_dec_btn = builder.get_object("btnSecondMinus")
        self.chkTimer = builder.get_object("chkTimer")
        self.lblTempo = builder.get_object("lblTempo")
        self.lblTempo2 = builder.get_object("lblTempo2")
        self.lblPonto1 = builder.get_object("lblPonto1")
        self.lblPonto2 = builder.get_object("lblPonto2")

        self.btnStart = builder.get_object("btnStart")
        self.btnStop = builder.get_object("btnStop")
        self.btnResume = builder.get_object("btnResume")
        self.btnQuit = builder.get_object("btnQuit")

        self.hours_inc_btn.connect("clicked", self.increment_hour)
        self.hours_dec_btn.connect("clicked", self.decrement_hour)

        self.minutes_inc_btn.connect("clicked", self.increment_minute)
        self.minutes_dec_btn.connect("clicked", self.decrement_minute)

        self.seconds_inc_btn.connect("clicked", self.increment_second)
        self.seconds_dec_btn.connect("clicked", self.decrement_second)

        self.btnStart.connect("clicked", self.on_start_button_clicked)
        self.btnStop.connect("clicked", self.on_btnStop_clicked)
        self.btnResume.connect("clicked", self.on_resume_button_clicked)
        self.btnQuit.connect("clicked", self.on_quit_button_clicked)

        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        self.timer_id = None
        self.last_update = 0

        builder.connect_signals(self)

        self.window = builder.get_object("Window")
        self.window.show_all()
        self.btnResume.set_visible(False)
        self.btnQuit.set_visible(False)
        self.lblTempo.set_visible(False)
        self.lblTempo2.set_visible(False)
        self.btnStop.set_sensitive(False)

        # CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(
            "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
        )

        self.entryHours.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.entryMinutes.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.entrySeconds.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.window.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.btnStart.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.btnStop.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.hours_inc_btn.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.hours_dec_btn.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.minutes_inc_btn.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.minutes_dec_btn.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.seconds_inc_btn.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.seconds_dec_btn.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def switch_interfaces(self, status) -> None:
        if status == 0:
            self.hours_inc_btn.set_visible(False)
            self.hours_dec_btn.set_visible(False)
            self.minutes_inc_btn.set_visible(False)
            self.minutes_dec_btn.set_visible(False)
            self.seconds_inc_btn.set_visible(False)
            self.seconds_dec_btn.set_visible(False)
            self.entryHours.set_visible(False)
            self.entryMinutes.set_visible(False)
            self.entrySeconds.set_visible(False)
            self.chkTimer.set_visible(False)
            self.lblPonto1.set_visible(False)
            self.lblPonto2.set_visible(False)
            self.lblTempo.set_visible(True)
            self.lblTempo2.set_visible(True)
        if status == 1:
            self.hours_inc_btn.set_visible(True)
            self.hours_dec_btn.set_visible(True)
            self.minutes_inc_btn.set_visible(True)
            self.minutes_dec_btn.set_visible(True)
            self.seconds_inc_btn.set_visible(True)
            self.seconds_dec_btn.set_visible(True)
            self.chkTimer.set_visible(True)
            self.entryHours.set_visible(True)
            self.entryMinutes.set_visible(True)
            self.entrySeconds.set_visible(True)
            self.lblPonto1.set_visible(True)
            self.lblPonto2.set_visible(True)
            self.lblTempo.set_visible(False)
            self.lblTempo2.set_visible(False)

    def show_label() -> None:
        # lblAviso.set_visible(True)
        # GLib.timeout_add_seconds(2, hide_label)
        pass

    def increment_hour(self, button):
        self.hours += 1
        self.entryHours.set_text("{:02d}".format(self.hours))

    def decrement_hour(self, button):
        if self.hours > 0:
            self.hours -= 1
            self.entryHours.set_text("{:02d}".format(self.hours))

    def increment_minute(self, button):
        self.minutes += 1
        self.entryMinutes.set_text("{:02d}".format(self.minutes))

    def decrement_minute(self, button):
        if self.minutes > 0:
            self.minutes -= 1
            self.entryMinutes.set_text("{:02d}".format(self.minutes))

    def increment_second(self, button):
        self.seconds += 1
        self.entrySeconds.set_text("{:02d}".format(self.seconds))

    def decrement_second(self, button):
        if self.seconds > 0:
            self.seconds -= 1
            self.entrySeconds.set_text("{:02d}".format(self.seconds))

    def timer(self, hours, minutes, seconds):
        total_seconds = hours * 3600 + minutes * 60 + seconds

        if total_seconds == 0:
            self.show_label()
            return False

        print(f"Timer Started: {hours} hours, {minutes} minutes, {seconds} seconds.")

        ending_time = get_timer_end(hours, minutes, seconds)
        update_timer_info(True, ending_time)

        self.btnStop.set_sensitive(True)
        self.btnStart.set_sensitive(False)
        self.switch_interfaces(0)
        self.countdown(total_seconds)
        if self.quit_event.is_set():
            print("Timer finalizado")
            self.btnStop.set_sensitive(False)
            self.switch_interfaces(1)
            return

        subprocess.run(["notify-send", "Focuseer", "Timer finished"])
        self.entryHours.set_text("00")
        self.entryMinutes.set_text("00")
        self.entrySeconds.set_text("00")
        self.btnStop.set_sensitive(False)
        self.btnStart.set_sensitive(True)
        self.switch_interfaces(1)

        if self.chkTimer.get_active() == False:
            mp3_file = "/home/marcos/Desktop/UNIP/tcc/nao_programacao/sounds/alarm.mp3"
            playsound(mp3_file)

    def countdown(self, total_seconds):
        while total_seconds > 0:
            if self.quit_event.is_set():
                return

            if not self.pause_event.is_set():
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                timer = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                print(timer, end="\r")
                self.lblTempo2.set_text(timer)
                time.sleep(1)
                total_seconds -= 1
            else:
                time.sleep(1)

    def pause_countdown(self):
        self.pause_event.set()
        self.btnResume.set_visible(True)
        self.btnQuit.set_visible(True)

    def resume_countdown(self):
        self.pause_event.clear()
        self.btnResume.set_visible(False)
        self.btnQuit.set_visible(False)
        self.btnStart.set_sensitive(False)

    def quit_countdown(self):
        self.quit_event.set()
        self.pause_event.set()
        self.entryHours.set_text("00")
        self.entryMinutes.set_text("00")
        self.entrySeconds.set_text("00")
        self.btnResume.set_visible(False)
        self.btnQuit.set_visible(False)
        self.btnStart.set_sensitive(True)
        update_timer_info(False, None)

    def on_start_button_clicked(self, button):
        if self.timer_thread and self.timer_thread.is_alive():
            # The timer is still running, terminate it gracefully
            self.quit_countdown()
            self.timer_thread.join()

        hours_text = self.entryHours.get_text()
        minutes_text = self.entryMinutes.get_text()
        seconds_text = self.entrySeconds.get_text()

        if (
            not hours_text.isdigit()
            or not minutes_text.isdigit()
            or not seconds_text.isdigit()
        ):
            print("Please enter valid integer values for the timer.")
            return

        hours = int(hours_text)
        minutes = int(minutes_text)
        seconds = int(seconds_text)

        # resolve o problema do timer nao funcionar uma segunda vez
        self.quit_event.clear()
        self.pause_event.clear()

        threading.Thread(target=self.timer, args=(hours, minutes, seconds)).start()

    def on_btnStop_clicked(self, button):
        self.pause_countdown()

    def on_resume_button_clicked(self, button):
        self.resume_countdown()

    def on_quit_button_clicked(self, button):
        self.quit_countdown()


if __name__ == "__main__":
    app = TimerApp()
    Gtk.main()
