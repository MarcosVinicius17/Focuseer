import json, io, base64
import matplotlib.pyplot as plt


def tempo_blacklist(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    # Get the date from the JSON
    date = data["day_data"]["date"]

    # Get the blacklist_data dictionary and sort it in ascending order by values
    blacklist_data = data["day_data"]["blacklist_data"]
    sorted_blacklist_data = sorted(blacklist_data.items(), key=lambda item: item[1])

    # Create the bar graph for blacklist data
    plt.bar(
        *zip(*sorted_blacklist_data), width=0.4
    )  # Adjust the width as per your preference
    plt.xlabel("Process")
    plt.ylabel("Value (Minutes)")
    plt.title(f"Blacklist Data for {date}")

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()

    buffer.seek(0)
    base64_image = base64.b64encode(buffer.getvalue()).decode()

    return base64_image


"""
Analisa o tempo gasto com aplicativos da whitelist. O resultado final deve ser em forma de graficos.
"""


def tempo_whitelist(json_file):
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


json_file = "/home/marcos/Desktop/UNIP/tcc/process_data.json"
# tempo_blacklist(json_file)
# tempo_whitelist(json_file)
