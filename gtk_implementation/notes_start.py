import gi, json

gi.require_version("Gtk", "3.0")
gi.require_version("GtkSource", "4")
gi.require_version("Pango", "1.0")
from gi.repository import Gtk, Gdk

import notes

# CSS
css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)

filename = "/home/marcos/Desktop/UNIP/tcc/banco_dados.json"


def open_notes(titulo, texto):
    notes.create_application(titulo, texto)


def procura_nota(titulo):
    with open(filename) as json_file:
        data = json.load(json_file)
        for i in data["notes"]:
            if i["titulo"] == titulo:
                print(f"Titulo:", i["titulo"], "Texto:", i["texto"], "Hora:", i["hora"])
                open_notes(i["titulo"], i["texto"])


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
        print("Clicked line:", line_num.get_line() + 1)
        print("Line text:", line_text)
        procura_nota(line_text)


"""temporario"""


def load_notes():
    # filename = "/home/marcos/Desktop/UNIP/tcc/banco_dados.json"
    titulos = []
    textos = []
    horas = []
    v = 1
    try:
        with open(filename) as json_file:
            if v == 0:
                print("Arquivo em branco")
            else:
                data = json.load(json_file)
                for p in data["notes"]:
                    textos.append(p["texto"])
                    titulos.append(p["titulo"])
                    horas.append(p["hora"])
                return (titulos, textos, horas)
    except FileNotFoundError:
        print("Arquivo nao localizado.")


"""
Carrega a lista de notas nas textViews
"""


def exibe_notas(window):
    titulos, textos, horas = load_notes()
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


textviewTitulo.connect("button-release-event", textview_click)


context_window = window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_textviewTitulo = textviewTitulo.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_textviewHora = textviewHora.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_lblHora = lblHora.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_lblTitulo = lblTitulo.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window.connect("realize", exibe_notas)
window.show_all()
Gtk.main()
