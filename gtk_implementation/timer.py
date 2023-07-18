import gi, time, subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from playsound import playsound

"""
simplify the code
"""


class TimerApp:
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("glade_screens/timer.glade")

        # self.window = self.builder.get_object("Window")
        self.window = builder.get_object("Window")
        self.hours_label = builder.get_object("hours")
        self.minutes_label = builder.get_object("minutes")
        self.seconds_label = builder.get_object("seconds")

        self.hours_inc_btn = builder.get_object("btnHourPlus")
        self.hours_dec_btn = builder.get_object("btnHourMinus")
        self.minutes_inc_btn = builder.get_object("btnMinutePlus")
        self.minutes_dec_btn = builder.get_object("btnMinuteMinus")
        self.seconds_inc_btn = builder.get_object("btnSecondPlus")
        self.seconds_dec_btn = builder.get_object("btnSecondMinus")
        self.chkTimer = builder.get_object("chkTimer")

        self.btnStart = builder.get_object("btnStart")
        self.btnStop = builder.get_object("btnStop")

        self.hours_inc_btn.connect("clicked", self.increment_hour)
        self.hours_dec_btn.connect("clicked", self.decrement_hour)

        self.minutes_inc_btn.connect("clicked", self.increment_minute)
        self.minutes_dec_btn.connect("clicked", self.decrement_minute)

        self.seconds_inc_btn.connect("clicked", self.increment_second)
        self.seconds_dec_btn.connect("clicked", self.decrement_second)

        # self.start_btn.connect("clicked", self.on_start_btn_clicked)
        self.btnStart.connect("clicked", self.start_timer)
        self.btnStop.connect("clicked", self.on_stop_btn_clicked)

        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        self.timer_id = None
        self.last_update = 0

        builder.connect_signals(self)

        self.window = builder.get_object("Window")
        self.window.show_all()

        # CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(
            "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
        )

        self.hours_label.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.minutes_label.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.seconds_label.get_style_context().add_provider(
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

    def increment_hour(self, button):
        self.hours += 1
        self.hours_label.set_text("{:02d}".format(self.hours))

    def decrement_hour(self, button):
        if self.hours > 0:
            self.hours -= 1
            self.hours_label.set_text("{:02d}".format(self.hours))

    def increment_minute(self, button):
        self.minutes += 1
        self.minutes_label.set_text("{:02d}".format(self.minutes))

    def decrement_minute(self, button):
        if self.minutes > 0:
            self.minutes -= 1
            self.minutes_label.set_text("{:02d}".format(self.minutes))

    def increment_second(self, button):
        self.seconds += 1
        self.seconds_label.set_text("{:02d}".format(self.seconds))

    def decrement_second(self, button):
        if self.seconds > 0:
            self.seconds -= 1
            self.seconds_label.set_text("{:02d}".format(self.seconds))

    def on_start_btn_clicked(self, button):
        if self.timer_id is not None:
            return

        total_seconds = self.hours * 3600 + self.minutes * 60 + self.seconds
        self.timer_id = GLib.timeout_add_seconds(1, self.update_timer, total_seconds)
        self.start_btn.set_label("Pause")

    def start_timer(self, widget):
        self.total_seconds = (self.hours * 3600) + (self.minutes * 60) + self.seconds
        self.last_update = int(time.time())

        # Call update_timer() every 1000 milliseconds (1 second)
        GLib.timeout_add(1000, self.update_timer)

    def on_stop_btn_clicked(self, button):
        if self.timer_id is None:
            return

        GLib.source_remove(self.timer_id)
        self.timer_id = None

        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        self.hours_label.set_text(str(self.hours))
        self.minutes_label.set_text(str(self.minutes))
        self.seconds_label.set_text(str(self.seconds))

        self.start_btn.set_label("Start")

    def update_timer(self):
        # Calculate time elapsed since last update
        current_time = int(time.time())
        elapsed_time = current_time - self.last_update

        # Calculate new total number of seconds left on the timer
        self.total_seconds -= elapsed_time
        if self.total_seconds < 0:
            self.total_seconds = 0

        # Check if timer has reached zero
        if self.total_seconds == 0:
            # self.on_stop_btn_clicked(None)

            if self.chkTimer.get_active():
                self.seconds_label.set_text("00")
                self.minutes_label.set_text("00")
                self.hours_label.set_text("00")
                subprocess.run(["notify-send", "Focuseer", "Timer finalizado"])

            else:
                self.seconds_label.set_text("00")
                self.minutes_label.set_text("00")
                self.hours_label.set_text("00")
                subprocess.run(["notify-send", "Focuseer", "Timer finalizado"])
                mp3_file = (
                    "/home/marcos/Desktop/UNIP/tcc/nao_programacao/sounds/alarm.mp3"
                )
                playsound(mp3_file)

            return False

        # Calculate hours, minutes, and seconds left
        self.hours = int(self.total_seconds / 3600)
        self.minutes = int((self.total_seconds % 3600) / 60)
        self.seconds = int(self.total_seconds % 60)

        # Update labels
        self.hours_label.set_text("{:02d}".format(self.hours))
        self.minutes_label.set_text("{:02d}".format(self.minutes))
        self.seconds_label.set_text("{:02d}".format(self.seconds))

        # Print progress to terminal
        print(f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}")

        # Update last update time
        self.last_update = current_time

        # Return True to continue updating the timer
        return True


if __name__ == "__main__":
    app = TimerApp()
    Gtk.main()
