import gi


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


builder = Gtk.Builder()
builder.add_from_file("glade_screens/trello_work.glade")

window = builder.get_object("Window")


css_provider = Gtk.CssProvider()

css_provider.load_from_path("gtk_implementation/custom_colors.css")

window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


window.show_all()


Gtk.main()
