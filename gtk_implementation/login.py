import gi, datetime, subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def login(button):
    print(txtLogin.get_text())
    print(f"password:", txtSenha.get_text())


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


css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/login_css.css"
)


context2 = btnCadastro.get_style_context()
context_window = window.get_style_context()
context3 = btnLogin.get_style_context()


context4 = txtLogin.get_style_context()
# context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

context_window.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
context2.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
context3.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


context4.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

window.show_all()

Gtk.main()
