import json
import matplotlib.pyplot as plt
from PIL import Image


def tempo_blacklist(json_file):
    print("\n\n metodo tempo_whitelist() \n\n")
    with open(json_file, "r") as file:
        data = json.load(file)

    date = data["tempo_gasto_processos"]["date"]

    whitelist_data = data["tempo_gasto_processos"]["blacklist_data"]

    # Replace None values with zero
    for key in whitelist_data:
        if whitelist_data[key] is None:
            whitelist_data[key] = 0

    sorted_whitelist_data = sorted(whitelist_data.items(), key=lambda item: item[1])

    try:
        plt.bar(*zip(*sorted_whitelist_data), width=0.4)
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
    print("\n\n metodo tempo_whitelist() \n\n")
    with open(json_file, "r") as file:
        data = json.load(file)

    date = data["tempo_gasto_processos"]["date"]

    whitelist_data = data["tempo_gasto_processos"]["whitelist_data"]

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
Analisa se o usuario alcancou as metas para o dia. Analisar o periodo de uma semana a um mes (verificar)
"""


def achieved_goal_rate(json_file):
    return


"""
Analisa o tempo gasto
"""


def time_spend_working(json_file):
    return


json_file = "gtk_implementation/reports/data.json"
