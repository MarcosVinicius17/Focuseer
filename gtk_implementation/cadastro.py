import gi, bcrypt
from pymongo import MongoClient

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def encriptar_senha(password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    print("Hashed password:", hashed_password.decode())
    return hashed_password


def cadastrar_usuario(button):
    nome = entryNome.get_text()
    login = entryLogin.get_text()
    password = entrySenha.get_text()
    confirm_password = entryConfirmaSenha.get_text()

    if password == confirm_password:
        hashed_password = encriptar_senha(password)

        """
        MongoDB stuff
        """
        client = MongoClient()
        # seleciona o database
        db = client.tcc_usuarios
        # seleciona a tabela
        users = db.users

        user1 = {
            "nome": nome,
            "login": login,
            "senha": hashed_password,
        }

        user_id = users.insert_one(user1).inserted_id

        print("Insert successful, here is the user id: ", user_id)

    else:
        print("wrong password")
        return


builder = Gtk.Builder()
builder.add_from_file("glade_screens/cadastro.glade")


window = builder.get_object("window")
entryNome = builder.get_object("entryNome")
entryLogin = builder.get_object("entryLogin")
entrySenha = builder.get_object("entrySenha")
entryConfirmaSenha = builder.get_object("entryConfirmaSenha")
btnCadastro = builder.get_object("btnCadastro")

btnCadastro.connect("clicked", cadastrar_usuario)

"""css stuff"""

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

context_entryNome = entryNome.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

context_entryLogin = entryLogin.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

context_entrySenha = entrySenha.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

context_entryConfirmaSenha = entryConfirmaSenha.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)


""" end of css"""


window.show_all()

Gtk.main()
