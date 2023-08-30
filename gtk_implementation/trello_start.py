import gi


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


builder = Gtk.Builder()
builder.add_from_file("glade_screens/trello_start.glade")

window = builder.get_object("Window")

entryApiKey = builder.get_object("entryApiKey")
entryApiSecret = builder.get_object("entryApiSecret")
entryToken = builder.get_object("entryToken")

btnIniciar = builder.get_object("btnIniciar")

css_provider = Gtk.CssProvider()

css_provider.load_from_path("gtk_implementation/custom_colors.css")

window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

entryApiKey.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
entryToken.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
entryApiSecret.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

btnIniciar.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window.show_all()


Gtk.main()
