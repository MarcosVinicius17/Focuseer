import gi, subprocess, sys
from pymongo import MongoClient

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


def store_api(button) -> None:
    client = MongoClient()
    db = client.tcc_usuarios
    apis = db.apis

    if entryApiKey.get_text() and entryApiSecret.get_text() and entryToken.get_text():
        api_entry = {
            "api_key": entryApiKey.get_text(),
            "api_secret": entryApiSecret.get_text(),
            "api_token": entryToken.get_text(),
        }

        api_insertion = apis.insert_one(api_entry).inserted_id
        print("API inserted into the DB")

        subprocess.Popen([sys.executable, "gtk_implementation/trello_work.py"])
        window.destroy()
    else:
        print("Campos em branco")


builder = Gtk.Builder()
builder.add_from_file("glade_screens/trello_start.glade")

window = builder.get_object("Window")

entryApiKey = builder.get_object("entryApiKey")
entryApiSecret = builder.get_object("entryApiSecret")
entryToken = builder.get_object("entryToken")

btnIniciar = builder.get_object("btnIniciar")
btnIniciar.connect("clicked", store_api)
btnLink = builder.get_object("btnLink")
btnLink.set_use_underline(False)


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

btnLink.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window.show_all()


Gtk.main()
