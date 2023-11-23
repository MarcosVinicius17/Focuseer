import gi
from trello import TrelloClient
from pymongo import MongoClient

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def get_stored_api() -> str:
    client = MongoClient()
    db = client.tcc_usuarios
    apis = db.apis

    api_values = apis.find_one({})

    if api_values:
        api_key = api_values.get("api_key")
        api_secret = api_values.get("api_secret")
        api_token = api_values.get("api_token")
        return api_key, api_secret, api_token
    else:
        print("Nenhuma API salva.")


credenciais = get_stored_api()
stored_api_key, stored_api_secret, stored_api_token = credenciais


client = TrelloClient(
    api_key=stored_api_key, api_secret=stored_api_secret, token=stored_api_token
)


def get_board_name(widget) -> str:
    dialog = Gtk.Dialog(
        title="Nome do board",
        buttons=(
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,
        ),
    )
    dialog.set_default_size(200, 50)

    # Create a text entry field
    entry = Gtk.Entry()
    entry.set_text("Nome do board")
    entry.set_activates_default(True)
    dialog.vbox.pack_start(entry, True, True, 0)
    entry.show()

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        text = entry.get_text()
        print("Board name:", text)
        lblBoard.set_text(text)
    dialog.destroy()

    get_boards_info(text)


def get_boards_info(board_name) -> None:
    boards = client.list_boards()
    for i in boards:
        if board_name == i.name:
            print("Board id:", i.id)
            get_itens(i.id)
        else:
            print(board_name, " não existe")


def get_itens(board_id):
    board = client.get_board(board_id)

    cards = board.get_cards()

    for card in cards:
        # print("Nome:", card.name)
        # print("ID", card.id)
        lista_ = card.get_list()
        # print("Lista:", lista_.name)
        if lista_.name == "A fazer":
            print("item da lista a fazer")
            label = Gtk.Label(card.name)
            label.set_line_wrap(True)
            listToDo.add(label)
            label.show_all()
        if lista_.name == "Sendo feitas":
            print("item da lista sendo feitas")
            label = Gtk.Label(card.name)
            label.set_line_wrap(True)
            listWorking.add(label)
            label.show_all()
        if lista_.name == "Concluidas":
            print("item da lista concluidas")
            label = Gtk.Label(card.name)
            label.set_line_wrap(True)
            listComplete.add(label)
            label.show_all()


builder = Gtk.Builder()
builder.add_from_file("glade_screens/trello_work.glade")

window = builder.get_object("Window")

lblBoard = builder.get_object("lblBoard")
listToDo = builder.get_object("listToDo")
listWorking = builder.get_object("listWorking")
listComplete = builder.get_object("listComplete")

css_provider = Gtk.CssProvider()

css_provider.load_from_path("gtk_implementation/custom_colors.css")

window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

lblBoard.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

listToDo.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

listComplete.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

listWorking.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window.connect("realize", get_board_name)

window.show_all()
Gtk.main()
