import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def salvarNota(button):
    print("salvo")


def on_day_selected(calendar):
    year, month, day = calendar.get_date()
    month += 1

    labelDia.set_text(f"{day:02}/{month:02}/{year}")


builder = Gtk.Builder()
builder.add_from_file("glade_screens/calendar.glade")


calendar = builder.get_object("calendar")

calendar.connect("day-selected", on_day_selected)


textView = builder.get_object("textview")


btnSalvar = builder.get_object("btnSalvar")
btnSalvar.connect("clicked", salvarNota)


window = builder.get_object("Window")

labelDia = builder.get_object("lblDia")

css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)

context_window = window.get_style_context()
context_calendar = calendar.get_style_context()
context_textview = textView.get_style_context()
context_btnSalvar = btnSalvar.get_style_context()

context_window.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
context_calendar.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
context_textview.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
context_btnSalvar.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

window.show_all()

Gtk.main()
