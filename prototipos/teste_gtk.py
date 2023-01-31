import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")

        self.label = Gtk.Label("Click the button to say hello!")
        self.button = Gtk.Button(label="Hello!")
        self.button.connect("clicked", self.on_button_clicked)

        self.box = Gtk.Box(spacing=6)
        self.box.pack_start(self.label, True, True, 0)
        self.box.pack_start(self.button, True, True, 0)

        self.add(self.box)

    def on_button_clicked(self, widget):
        self.label.set_text("Hello, World!")


win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
