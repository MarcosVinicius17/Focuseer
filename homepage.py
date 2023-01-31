import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

"""
Depois de fazer a GUI com o Glade, suas funcionalidades sao implantadas deste jeito.
Deve-se carregar o arquivo .glade e entao ir modificando-o.
"""


def alarm(button):
    print("alarm")


builder = Gtk.Builder()
builder.add_from_file("homepage.glade")

window = builder.get_object("Window")


btnAlarm = builder.get_object("btnAlarm")
btnAlarm.connect("clicked", alarm)


"""
Exibir a janela
"""

window.show_all()

Gtk.main()
