import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def on_checkbox_toggled(checkbox):
    label = checkbox.get_label()
    status = "checked" if checkbox.get_active() else "unchecked"
    print("Checkbox:", label, "- Status:", status)


def add_permitido(process):
    checkbox = Gtk.CheckButton(label=process)
    listPermitidos.add(checkbox)
    checkbox.connect("toggled", on_checkbox_toggled)


def add_nao_permitido(process):
    checkbox = Gtk.CheckButton(label=process)
    listNaoPermitidos.add(checkbox)
    checkbox.connect("toggled", on_checkbox_toggled)


css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)

builder = Gtk.Builder()
builder.add_from_file("glade_screens/monitor.glade")

window = builder.get_object("window")
btnEditPermitidos = builder.get_object("btnEditPermitidos")
btnEditNaoPermitidos = builder.get_object("btnEditNaoPerm")
listPermitidos = builder.get_object("listPermitidos")
listNaoPermitidos = builder.get_object("listNaoPermitidos")
btnAttPermitidos = builder.get_object("btnAttPermitidos")
btnAttNaoPermitidos = builder.get_object("btnAttNaoPermitidos")

context_window = window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnPermitidos = btnEditPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnEditNaoPermitidos = btnEditNaoPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_listPermitidos = listPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

context_listNaoPermitidos = listNaoPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

context_btnAttNaoPermitidos = btnAttNaoPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

context_btnAttPermitidos = btnAttPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


add_nao_permitido("steam")
add_permitido("VSCode")
add_permitido("Teams")
add_nao_permitido("Spotify")
window.show_all()
Gtk.main()
