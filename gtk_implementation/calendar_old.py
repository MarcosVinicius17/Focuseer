import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
import calendar
import os


class CalendarWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Calendar")
        self.set_default_size(600, 400)

        self.calendar = Gtk.Calendar()
        self.calendar.set_hexpand(True)
        self.calendar.set_vexpand(True)
        self.calendar.connect("day-selected", self.on_day_selected)

        self.textview = Gtk.TextView()
        self.textview.set_hexpand(True)
        self.textview.set_vexpand(True)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        scrolled_window.add(self.textview)

        button = Gtk.Button(label="Save")
        button.connect("clicked", self.on_save_clicked)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(self.calendar, True, True, 0)
        box.pack_start(scrolled_window, True, True, 0)
        box.pack_start(button, False, True, 0)

        self.add(box)

    def on_day_selected(self, widget):
        year, month, day = self.calendar.get_date()
        month += 1  # Gtk.Calendar months are 0-based

        print(f"Day selected: {year}-{month:02}-{day:02}")

    def on_save_clicked(self, button):
        print("clickado")


win = CalendarWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
