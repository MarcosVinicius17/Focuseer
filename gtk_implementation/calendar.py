import gi, locale
from pymongo import MongoClient

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

gi.require_version("Pango", "1.0")

# Traduz os dias da semana
locale.setlocale(locale.LC_ALL, "pt_BR.utf8")


def salvarNota(button) -> None:
    """MongoDB stuff"""
    client = MongoClient()
    db = client.tcc_usuarios
    note = db.calendar_notes

    """Getting the content"""
    buffer = textView.get_buffer()
    start_iter = buffer.get_start_iter()
    end_iter = buffer.get_end_iter()
    text = buffer.get_text(start_iter, end_iter, False)
    current_date = labelDia.get_text()

    """Create or update if already exists"""

    old_note = note.find_one({"data": current_date})

    if old_note:
        note_update = note.find_one_and_update(old_note, {"$set": {"mensagem": text}})

    else:
        note_to_insert = {"data": current_date, "mensagem": text}

        note_id = note.insert_one(note_to_insert).inserted_id
        print("Insert successful, here is the user id: ", note_id)


def get_text_from_day() -> None:
    client = MongoClient()
    db = client.tcc_usuarios
    note = db.calendar_notes

    current_date = labelDia.get_text()

    note_content = note.find_one({"data": current_date})

    if note_content:
        mensagem = note_content["mensagem"]
        buffer = textView.get_buffer()
        buffer.set_text(mensagem)
    else:
        buffer = textView.get_buffer()
        buffer.set_text("")


def on_day_selected(calendar) -> None:
    year, month, day = calendar.get_date()
    month += 1

    labelDia.set_text(f"{day:02}/{month:02}/{year}")
    get_text_from_day()


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
