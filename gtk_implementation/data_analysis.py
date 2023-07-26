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

    # Get the process_data dictionary and sort it in ascending order by values
    process_data = data["day_data"]["process_data"]
    sorted_data = sorted(process_data.items(), key=lambda item: item[1])

    items, values = zip(*sorted_data)

    # Convert the values from seconds to minutes
    values_in_minutes = [value / 60 for value in values]

    # Create a bar graph with thinner bars
    plt.bar(
        items, values_in_minutes, width=0.4
    )  # Adjust the width as per your preference
    plt.xlabel("Process")
    plt.ylabel("Value (Minutes)")
    plt.title(f"Data for {date}")
    plt.show()


"""
Analisa o tempo gasto com aplicativos da whitelist. O resultado final deve ser em forma de graficos.
"""


def whitelisted_process_time(json_file):
    return


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
