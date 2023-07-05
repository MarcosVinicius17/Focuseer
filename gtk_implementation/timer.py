import gi, time, subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

"""
Funciona, mas esta complicado ate dms
REFATORAR!
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

        self.btnStart = builder.get_object("btnStart")
        self.btnStop = builder.get_object("btnStop")

        self.hours_inc_btn.connect("clicked", self.on_hours_inc_btn_clicked)
        self.hours_dec_btn.connect("clicked", self.on_hours_dec_btn_clicked)

        self.minutes_inc_btn.connect("clicked", self.on_minutes_inc_btn_clicked)
        self.minutes_dec_btn.connect("clicked", self.on_minutes_dec_btn_clicked)

        self.seconds_inc_btn.connect("clicked", self.on_seconds_inc_btn_clicked)
        self.seconds_dec_btn.connect("clicked", self.on_seconds_dec_btn_clicked)

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

    def on_hours_inc_btn_clicked(self, button):
        self.hours += 1
        self.hours_label.set_text("{:02d}".format(self.hours))

    def on_hours_dec_btn_clicked(self, button):
        if self.hours > 0:
            self.hours -= 1
            self.hours_label.set_text("{:02d}".format(self.hours))

    def on_minutes_inc_btn_clicked(self, button):
        self.minutes += 1
        self.minutes_label.set_text("{:02d}".format(self.minutes))

    def on_minutes_dec_btn_clicked(self, button):
        if self.minutes > 0:
            self.minutes -= 1
            self.minutes_label.set_text("{:02d}".format(self.minutes))

    def on_seconds_inc_btn_clicked(self, button):
        self.seconds += 1
        self.seconds_label.set_text("{:02d}".format(self.seconds))

    def on_seconds_dec_btn_clicked(self, button):
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
            subprocess.run(["notify-send", "Focuseer", "Timer finalizado!"])

            self.seconds_label.set_text("00")
            self.minutes_label.set_text("00")
            self.hours_label.set_text("00")

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
