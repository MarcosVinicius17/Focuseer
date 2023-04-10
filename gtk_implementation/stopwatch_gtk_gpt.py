import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import time


class Stopwatch:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("glade_screens/stopwatch.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("Window")
        self.label_hours = self.builder.get_object("lblHours")
        self.label_minutes = self.builder.get_object("lblMinutes")
        self.label_seconds = self.builder.get_object("lblSeconds")
        self.start_button = self.builder.get_object("btnStart")
        self.pause_button = self.builder.get_object("btnStop")
        self.is_running = False
        self.start_time = 0

        self.start_button.connect("clicked", self.on_start_button_clicked)
        self.pause_button.connect("clicked", self.on_pause_button_clicked)

    def on_start_button_clicked(self, button):
        self.is_running = True
        self.start_time = time.time()
        self.update_stopwatch()

    def on_pause_button_clicked(self, button):
        if self.is_running:
            self.is_running = False
            button.set_label("Reset")
        else:
            self.is_running = False
            button.set_label("Pause")
            self.label_hours.set_text("00")
            self.label_minutes.set_text("00")
            self.label_seconds.set_text("00")

    def update_stopwatch(self):
        if self.is_running:
            elapsed_time = time.time() - self.start_time
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            self.label_hours.set_text(str(hours).zfill(2))
            self.label_minutes.set_text(str(minutes).zfill(2))
            self.label_seconds.set_text(str(seconds).zfill(2))
            print(
                f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"
            )
            GLib.timeout_add(1000, self.update_stopwatch)

    def on_window_destroy(self, window):
        Gtk.main_quit()


if __name__ == "__main__":
    app = Stopwatch()
    app.window.show_all()
    Gtk.main()
