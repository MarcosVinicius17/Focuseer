from trello import TrelloClient


client = TrelloClient(
    api_key="d811868a9f5ac9791218fc1a5b922b8a",
    api_secret="33d56f46983aebecf60c75f8d5ec3615976508244b8c0cbb50db472285b196ce",
    token="ATTAcb21b5901cbc4fb1d8a29db58ba6d4a95a3cc658784b40f5004807f67c9bd598031E98F5",
    token_secret=None,
)


# exemplo
# board_name = "Teste_api"
def get_board_info(board_name):
    # Find the board by name
    board = board_name
    for b in client.list_boards():
        if b.name == board_name:
            board = b
            break

    if board:
        print(f"Board '{board_name}' encontrado.")
        print(f"ID : {board.id}")
        print(f"URL: {board.url}")
        print("Listas:")
        for l in board.list_lists():
            print(f"- Lista: {l.name}")
            print("  Cartoes:")
            for card in l.list_cards():
                print(f"  - {card.name}")
    else:
        print(f"Board '{board_name}' não encontrado")


def add_card_to_list(board_name, card_name, card_description, list_name):
    board = None
    for b in client.list_boards():
        if b.name == board_name:
            board = b
            break

    if board:
        todo_list = None
        for l in board.list_lists():
            if l.name == list_name:
                todo_list = l
                break

        if todo_list:
            card = todo_list.add_card(card_name, card_description)
            print(f"Cartão '{card_name}' adicionado a lista {list_name}")
        else:
            print(f"Lista {list_name} não encontrada.")
    else:
        print(f"Board '{board_name}' não encontrado.")


"""board_name = "Teste_api"
card_name = "GTK"
card_description = "Criar janela GTK"
add_card_to_list(board_name, card_name, card_description, "Sendo feitas")"""

"""
transfere um card da lista A para lista B
"""


def transfer_card(board_name, card_name, from_list_name, to_list_name):
    board = None
    for b in client.list_boards():
        if b.name == board_name:
            board = b
            break

    if board:
        from_list = None
        to_list = None

        for l in board.list_lists():
            if l.name == from_list_name:
                from_list = l
            elif l.name == to_list_name:
                to_list = l

        if from_list and to_list:
            for card in from_list.list_cards():
                if card.name == card_name:
                    card.change_list(to_list.id)
                    print(
                        f"Card '{card_name}' transferred from '{from_list_name}' to '{to_list_name}'."
                    )
                    break
            else:
                print(f"Card '{card_name}' not found in '{from_list_name}'.")
        else:
            print("Source or destination lists not found on the board.")
    else:
        print(f"Board '{board_name}' not found.")


# Usage
"""board_name = "Teste_api"
card_name = "Transferir"
from_list_name = "A fazer"
to_list_name = "Concluidas"
transfer_card(board_name, card_name, from_list_name, to_list_name)"""
