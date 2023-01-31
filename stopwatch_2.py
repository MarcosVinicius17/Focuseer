import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Glade Example")

        builder = Gtk.Builder()
        builder.add_from_file("stopwatch.glade")
        self.window = builder.get_object("Window")

        # Connect signals
        builder.connect_signals(self)

        # Get a reference to the label
        self.hours = builder.get_object("lblHours")
        self.minutes = builder.get_object("lblMinutes")
        self.seconds = builder.get_object("lblSeconds")


if __name__ == "__main__":
    win = MyWindow()
    win.show_all()
    Gtk.main()
