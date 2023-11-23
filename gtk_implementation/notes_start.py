import gi, subprocess, sys
from pymongo import MongoClient

gi.require_version("Gtk", "3.0")
gi.require_version("GtkSource", "4")
gi.require_version("Pango", "1.0")
from gi.repository import Gtk, Gdk

import notes
import locale

locale.setlocale(locale.LC_ALL, "pt_BR.utf8")


# CSS
css_provider = Gtk.CssProvider()
css_provider.load_from_path("gtk_implementation/custom_colors.css")


def open_blank_note(button):
    window.hide()
    subprocess.Popen([sys.executable, "gtk_implementation/notes.py"])
    window.show()


def open_notes(titulo, texto):
    # window.destroy()
    # window.hide()
    notes.create_application(titulo, texto)
    # window.show()


def procura_nota(titulo):
    client = MongoClient()
    db = client.tcc_usuarios
    notes = db.notes

    nota = notes.find_one({"titulo": titulo})

    if nota:
        pass
    else:
        print("nota nao existe")

    open_notes(nota["titulo"], nota["texto"])


"""
Quando o usuario aperta uma linha
"""


def textview_click(textview, event):
    if event.button == Gdk.BUTTON_PRIMARY:
        # Get the clicked position
        x, y = textview.window_to_buffer_coords(
            Gtk.TextWindowType.WIDGET, int(event.x), int(event.y)
        )
        buffer = textview.get_buffer()
        insert_mark = buffer.get_insert()
        iter = buffer.get_iter_at_mark(insert_mark)
        line_num = buffer.get_iter_at_line(iter.get_line())
        line_start = line_num.copy()
        line_end = line_start.copy()
        line_end.forward_to_line_end()

        line_text = buffer.get_text(line_start, line_end, False)

        procura_nota(line_text)


def carregar_notas():
    titulos = []
    textos = []
    horas = []

    client = MongoClient()
    db = client.tcc_usuarios
    notes = db.notes

    cursor = notes.find({})

    for i in cursor:
        titulos.append(i["titulo"])
        textos.append(i["texto"])
        horas.append(i["hora"])
    return titulos, textos, horas


def exibe_notas(window):
    titulos, textos, horas = carregar_notas()
    buffer = textviewTitulo.get_buffer()
    buffer_hora = textviewHora.get_buffer()

    for i in titulos:
        buffer.insert(buffer.get_end_iter(), i + "\n")
    for j in horas:
        buffer_hora.insert(buffer_hora.get_end_iter(), j + "\n")

    textviewHora.set_editable(False)
    textviewTitulo.set_editable(False)


builder = Gtk.Builder()
builder.add_from_file("glade_screens/notes_start.glade")


window = builder.get_object("window")
textviewTitulo = builder.get_object("textviewTitulo")
textviewHora = builder.get_object("textviewHora")
lblTitulo = builder.get_object("lblTitulo")
lblHora = builder.get_object("lblHora")
btnAddNote = builder.get_object("btnAddNote")

btnAddNote.connect("clicked", open_blank_note)
textviewTitulo.connect("button-release-event", textview_click)


window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
textviewTitulo.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
textviewHora.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
lblHora.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
lblTitulo.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

btnAddNote.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window.connect("realize", exibe_notas)
window.show_all()
Gtk.main()
