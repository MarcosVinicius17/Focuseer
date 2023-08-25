from weasyprint import HTML
from jinja2 import Template
from datetime import datetime
import data_analysis
import os, json


# temporario
# json_file = "/home/marcos/Desktop/UNIP/tcc/process_data.json"
json_file = "gtk_implementation/temp_data.json"


def tempo_trabalhado(inicio, final):
    try:
        # separa horas de minutos utilizando
        horas1, minutos1 = map(int, inicio.split(":"))
        horas2, minutos2 = map(int, final.split(":"))

        # tempo total em minutos
        total_minutos1 = horas1 * 60 + minutos1
        total_minutos2 = horas2 * 60 + minutos2

        diferenca_minutos = total_minutos2 - total_minutos1

        # para quando o horario final vem antes do de inicio
        if diferenca_minutos < 0:
            diferenca_minutos += 24 * 60

        # converte o resultado para horas e minutos
        diferenca_hr = diferenca_minutos // 60
        diferenca_mn = diferenca_minutos % 60

        diferenca = f"{diferenca_hr:02d}:{diferenca_mn:02d}"
        return diferenca
    except ValueError:
        return "Formato invalido. Use o formato HH:MM "


def generate_pdf(html_template):
    # Load the Jinja2 environment and the HTML template
    env = Template(html_template)

    with open("gtk_implementation/temp_data.json", "r") as file:
        data = json.load(file)

        nome = data["objetivos_dia"]["nome_usuario"]
        tempo_gasto = data["objetivos_dia"]["tempo_gasto"]
        completion_rate = data["objetivos_dia"]["completion_rate"]
        hora_encerramento = data["hora_encerramento"]["hora"]

    now = datetime.now()
    hora_emissao = now.strftime("%d/%m/%Y - %H:%M")
    archive_name = now.strftime("%d_%m_%Y_%H_%M")

    # exemples
    # data_criacao = formatted_date
    data_criacao = "$$;$$"
    hora_entrada = "08:30"
    hora_saida = "17:30"
    previous_time = "07:30"
    week_time_spent = "07:30"
    whitelist_graphic = data_analysis.tempo_whitelist(json_file)
    blacklist_graphic = data_analysis.tempo_blacklist(json_file)

    tempo_gasto = tempo_trabalhado(hora_entrada, hora_saida)

    # Associa as variaveis
    html_out = env.render(
        nome_usuario=nome,
        hora_emissao=hora_emissao,
        inicio=hora_entrada,
        fim=hora_saida,
        week_average_time=week_time_spent,
        whitelist_graph=whitelist_graphic,
        blacklist_graph=blacklist_graphic,
        time_spent=tempo_gasto,
        rate_completion=completion_rate,
        whitelist_time_spent="$$",
        blacklist_time_spent="$$",
    )

    """html_out = env.render(
        nome=nome,
        data_criacao=data_criacao,
        hora_entrada=hora_entrada,
        hora_saida=hora_saida,
        previous_time=previous_time,
        week_time_spent=week_time_spent,
        whitelist_graph=whitelist_graphic,
        blacklist_graph=blacklist_graphic,
        time_spent=tempo_gasto,
    )"""

    # Cria o PDF
    with open("gtk_implementation/pdf_creator/relatorio.html", "w") as f:
        f.write(html_out)

    HTML(filename="gtk_implementation/pdf_creator/relatorio.html").write_pdf(
        archive_name + ".pdf"
    )
    print(archive_name, "PDF has been created")
    os.remove("blacklist_graph.png")
    os.remove("whitelist_graph.png")


if __name__ == "__main__":
    with open("gtk_implementation/pdf_creator/relatorio.html", "r") as f:
        html_template = f.read()

    generate_pdf(html_template)
