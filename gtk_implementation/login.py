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
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)


context_btnCadastro = btnCadastro.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_window = window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnLogin = btnLogin.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_txtLogin = txtLogin.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_txtSenha = txtSenha.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


window.show_all()

Gtk.main()
