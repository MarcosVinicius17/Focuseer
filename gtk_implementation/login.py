import gi, datetime, subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def login(button):
    print("login")


def cadastro(button):
    print("cadastro")


builder = Gtk.Builder()
builder.add_from_file("glade_screens/login.glade")

window = builder.get_object("Window")

txtLogin = builder.get_object("txtLogin")
txtSenha = builder.get_object("txtSenha")

btnLogin = builder.get_object("btnLogin")
btnLogin.connect("clicked", login)


btnCadastro = builder.get_object("btnCadastro")
btnCadastro.connect("clicked", cadastro)

window.show_all()

Gtk.main()
