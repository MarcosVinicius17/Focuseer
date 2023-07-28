"""'
Contem os metodos que analisam os dados do usuario (principalmente os provenientes do monitor de processos) para a criacao de graficos e estatisticas
"""
import json
from pymongo import MongoClient
import matplotlib.pyplot as plt


"""
Analisa o tempo gasto com aplicativos da blacklist. O resultado final deve ser em forma de graficos.
"""


def blacklisted_process_time(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    # Get the date from the JSON
    date = data["day_data"]["date"]

    # Get the blacklist_data dictionary and sort it in ascending order by values
    blacklist_data = data["day_data"]["blacklist_data"]
    sorted_blacklist_data = sorted(blacklist_data.items(), key=lambda item: item[1])

    # Convert the values from seconds to minutes for blacklist data
    blacklist_values_in_minutes = [value / 60 for value in blacklist_data.values()]

    # Create the bar graph for blacklist data
    plt.bar(
        *zip(*sorted_blacklist_data), width=0.4
    )  # Adjust the width as per your preference
    plt.xlabel("Process")
    plt.ylabel("Value (Minutes)")
    plt.title(f"Blacklist Data for {date}")
    plt.show()


"""
Analisa o tempo gasto com aplicativos da whitelist. O resultado final deve ser em forma de graficos.
"""


def whitelisted_process_time(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    # Get the date from the JSON
    date = data["day_data"]["date"]

    # Get the whitelist_data dictionary and sort it in ascending order by values
    whitelist_data = data["day_data"]["whitelist_data"]
    sorted_whitelist_data = sorted(whitelist_data.items(), key=lambda item: item[1])

    # Convert the values from seconds to minutes for whitelist data
    # whitelist_values_in_minutes = [value / 60 for value in whitelist_data.values()]

    # Create the bar graph for whitelist data
    plt.bar(
        *zip(*sorted_whitelist_data), width=0.4
    )  # Adjust the width as per your preference
    plt.xlabel("Process")
    plt.ylabel("Value (Minutes)")
    plt.title(f"Whitelist Data for {date}")
    plt.show()


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


# Example usage:
json_file = "/home/marcos/Desktop/UNIP/tcc/process_data.json"
blacklisted_process_time(json_file)
whitelisted_process_time(json_file)
