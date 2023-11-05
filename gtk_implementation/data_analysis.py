import json
import matplotlib.pyplot as plt
from PIL import Image


def tempo_blacklist(json_file):
    print("metodo tempo_blacklist()")
    with open(json_file, "r") as file:
        data = json.load(file)

    date = data["tempo_gasto_processos"]["date"]

    blacklist_data = data["tempo_gasto_processos"]["blacklist_data"]

    if not blacklist_data:
        print("No data to create the graph.")
        return None

    # Replace None values with zero
    for key in blacklist_data:
        if blacklist_data[key] is None:
            blacklist_data[key] = 0

    sorted_blacklist_data = sorted(blacklist_data.items(), key=lambda item: item[1])

    try:
        plt.bar(*zip(*sorted_blacklist_data), width=0.4)
        plt.xlabel("Processo")
        plt.ylabel("Tempo (Em minutos)")
        plt.title(f"Blacklist Data for {date}")

        image_path = "blacklist_graph.png"
        plt.savefig(image_path, format="png")
        plt.close()

        image = Image.open(image_path)
        new_height = int(image.height * 0.7)
        new_width = int(image.width * 0.7)
        resized_img = image.resize((new_width, new_height), Image.ANTIALIAS)
        resized_img.save("blacklist_graph.png", format="png")
        print("blacklist criado")
        image.close()

        return image_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def tempo_whitelist(json_file):
    print("metodo tempo_whitelist()")
    with open(json_file, "r") as file:
        data = json.load(file)

    date = data["tempo_gasto_processos"]["date"]

    whitelist_data = data["tempo_gasto_processos"]["whitelist_data"]

    if not whitelist_data:
        print("No data to create the graph.")
        return None

    # Replace None values with zero
    for key in whitelist_data:
        if whitelist_data[key] is None:
            whitelist_data[key] = 0

    sorted_whitelist_data = sorted(whitelist_data.items(), key=lambda item: item[1])

    try:
        plt.bar(*zip(*sorted_whitelist_data), width=0.4)
        plt.xlabel("Processo")
        plt.ylabel("Tempo (Em minutos)")
        plt.title(f"Whitelist Data for {date}")

        image_path = "whitelist_graph.png"
        plt.savefig(image_path, format="png")
        plt.close()

        image = Image.open(image_path)
        new_height = int(image.height * 0.7)
        new_width = int(image.width * 0.7)
        resized_img = image.resize((new_width, new_height), Image.ANTIALIAS)
        resized_img.save("whitelist_graph.png", format="png")
        print("whitelist criado")
        image.close()

        return image_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


"""
Analisa o tempo gasto
"""


def whitelist_time_spent(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    whitelist_data = data.get("tempo_gasto_processos", {}).get("whitelist_data", {})

    total_sum = sum(whitelist_data.values())
    return total_sum


def blacklist_time_spent(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    blacklist_data = data.get("tempo_gasto_processos", {}).get("blacklist_data", {})

    total_sum = sum(blacklist_data.values())
    return total_sum


def time_spend_working(json_file):
    return


json_file = "gtk_implementation/reports/data.json"
