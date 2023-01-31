import time, gi

from gi.repository import Gtk


class Stopwatch:
    def __init__(self):
        # Load the .glade file
        builder = Gtk.Builder()
        builder.add_from_file("stopwatch.glade")

        # Get the labels for hours, minutes, and seconds
        self.hours_label = builder.get_object("lblHours")
        self.minutes_label = builder.get_object("lblMinutes")
        self.seconds_label = builder.get_object("lblSeconds")

        # Get the start and stop buttons
        start_button = builder.get_object("btnStart")
        # stop_button = builder.get_object("stop_button")

        # Connect the signals
        start_button.connect("clicked", self.on_start_clicked)
        # stop_button.connect("clicked", self.on_stop_clicked)

        # Show the window
        window = builder.get_object("stopwatch_window")
        window.show_all()

        # Set the initial time to 0
        self.start_time = 0
        self.stop_time = 0

    def on_start_clicked(self, button):
        # Start the timer
        self.start_time = time.time()

    def on_stop_clicked(self, button):
        # Stop the timer
        self.stop_time = time.time()

    def update_time(self):
        # Calculate the elapsed time
        elapsed_time = self.stop_time - self.start_time

        # Convert the elapsed time to hours, minutes, and seconds
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Update the labels
        self.hours_label.set_text(str(int(hours)))
        self.minutes_label.set_text(str(int(minutes)))
        self.seconds_label.set_text(str(int(seconds)))


if __name__ == "__main__":
    stopwatch = Stopwatch()
    Gtk.main()
