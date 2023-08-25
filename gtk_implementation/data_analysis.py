import json
import matplotlib.pyplot as plt
from PIL import Image


def tempo_blacklist(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    # Get the date from the JSON
    date = data["tempo_gasto_processos"]["date"]

    # Get the blacklist_data dictionary and sort it in ascending order by values
    blacklist_data = data["tempo_gasto_processos"]["blacklist_data"]
    sorted_blacklist_data = sorted(blacklist_data.items(), key=lambda item: item[1])

    # Create the bar graph for blacklist data
    plt.bar(
        *zip(*sorted_blacklist_data), width=0.4
    )  # Adjust the width as per your preference
    plt.xlabel("Processo")
    plt.ylabel("Tempo (Em minutos)")
    plt.title(f"Blacklist Data for {date}")

    image_path = "blacklist_graph.png"
    plt.savefig(image_path, format="png", dpi=100)
    plt.close()
    image = Image.open(image_path)
    new_height = int(image.height * 0.7)
    new_width = int(image.width * 0.7)
    resized_img = image.resize((new_width, new_height), Image.ANTIALIAS)
    resized_img.save("blacklist_graph.png", format="png")

    image.close()

    return image_path


def tempo_whitelist(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    date = data["tempo_gasto_processos"]["date"]

    whitelist_data = data["tempo_gasto_processos"]["whitelist_data"]
    sorted_whitelist_data = sorted(whitelist_data.items(), key=lambda item: item[1])

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

    image.close()

    return image_path


"""
Analisa se o usuario alcancou as metas para o dia. Analisar o periodo de uma semana a um mes (verificar)
"""


def achieved_goal_rate(json_file):
    return


"""
Analisa o tempo gasto
"""


def time_spend_working(json_file):
    return


json_file = "/home/marcos/Desktop/UNIP/tcc/process_data.json"
