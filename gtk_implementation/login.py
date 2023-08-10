import gi, bcrypt, subprocess, sys
from pymongo import MongoClient

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from homepage import set_headerbar_title


def hide_label() -> False:
    lblSenha.hide()
    return False


def show_label() -> None:
    lblSenha.set_visible(True)
    GLib.timeout_add_seconds(2, hide_label)


def verifica_senha(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode(), hashed_password)


def login(button) -> None:
    client = MongoClient()
    db = client.tcc_usuarios
    users = db.users
    user = users.find_one({"login": txtLogin.get_text()})

    password = txtSenha.get_text()

    # se o usuario existe no BD
    if user:
        print("user found")
        hashed_password = user["senha"]
        username = user["nome"]
        pw_match = verifica_senha(password, hashed_password)

        if pw_match:
            subprocess.Popen([sys.executable, "gtk_implementation/homepage.py"])
            set_headerbar_title(username)
            window.destroy()
        else:
            lblSenha.set_text("Senha incorreta")
            show_label()

    else:
        lblSenha.set_text("Usuário não encontrado")
        show_label()


def cadastro(button) -> None:
    subprocess.Popen([sys.executable, "gtk_implementation/cadastro.py"])


builder = Gtk.Builder()
builder.add_from_file("glade_screens/login.glade")

window = builder.get_object("Window")

txtLogin = builder.get_object("txtLogin")
txtSenha = builder.get_object("txtSenha")

btnLogin = builder.get_object("btnLogin")
btnLogin.connect("clicked", login)


btnCadastro = builder.get_object("btnCadastro")
btnCadastro.connect("clicked", cadastro)

lblSenha = builder.get_object("lblSenha")


css_provider = Gtk.CssProvider()

css_provider.load_from_path("gtk_implementation/custom_colors.css")


btnCadastro.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnLogin.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
txtLogin.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
txtSenha.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


window.show_all()
lblSenha.set_visible(False)

Gtk.main()
