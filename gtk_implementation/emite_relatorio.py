from weasyprint import HTML
from jinja2 import Template
from datetime import datetime
import data_analysis
import os, json, shutil

from pymongo import MongoClient


def store_report_address(address, hour):
    client = MongoClient()
    db = client.tcc_usuarios
    reports = db.reports

    print(f"salvando item {address} gerado as {hour}")
    report = {"data_emissao": hour, "endereco": address}

    report_id = reports.insert_one(report).inserted_id
    print(report_id)


json_file = "gtk_implementation/reports/data.json"


"""Creates a copy of the HTML template to edit"""


def copy_template():
    source = "gtk_implementation/reports/report_with_pic.html"
    report_copy = "gtk_implementation/reports/relatorio_copia.html"
    shutil.copy(source, report_copy)


"""calcula a diferenca entre hora do fim e inicio"""


def tempo_trabalhado(inicio, final):
    print(f"Inicio:{inicio} Final: {final} ")
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
    print("metodo generate_pdf()")
    # Load the Jinja2 environment and the HTML template
    env = Template(html_template)

    with open("gtk_implementation/reports/data.json", "r") as file:
        data = json.load(file)

        nome = data["objetivos_dia"]["nome_usuario"]
        tempo_gasto = data["objetivos_dia"]["tempo_gasto"]
        completion_rate = data["objetivos_dia"]["completion_rate"]
        completion_rate_formatted = round(completion_rate, 2)
        hora_encerramento = data["hora_encerramento"]["hora"]

    now = datetime.now()
    hora_emissao = now.strftime("%d/%m/%Y - %H:%M")
    archive_name = now.strftime("%d_%m_%Y_%H_%M")

    # exemples
    # data_criacao = formatted_date

    hora_entrada = hora_emissao
    hora_saida = hora_encerramento

    whitelist_graph = data_analysis.generate_whitelist_graph(json_file)

    blacklist_graph = data_analysis.generate_blacklist_graph(json_file)

    tempo_gasto = tempo_trabalhado(hora_entrada, hora_saida)

    # Associa as variaveis
    html_out = env.render(
        nome_usuario=nome,
        hora_emissao=hora_emissao,
        hora_inicio=hora_entrada,
        hora_final=hora_saida,
        # whitelist_graph=whitelist_graph,
        # blacklist_graph=blacklist_graph,
        blacklist_graphic="/home/marcos/Desktop/UNIP/tcc/blacklist_graph.png",
        whitelist_graphic="/home/marcos/Desktop/UNIP/tcc/whitelist_graph.png",
        total_time_spent=tempo_gasto,
        completion_rate=completion_rate_formatted,
        whitelist_time=data_analysis.whitelist_time_spent(
            "gtk_implementation/reports/data.json"
        ),
        blacklist_time=data_analysis.blacklist_time_spent(
            "gtk_implementation/reports/data.json"
        ),
    )

    # Cria o PDF
    copy_template()
    with open("gtk_implementation/reports/relatorio_copia.html", "w") as f:
        f.write(html_out)

    HTML(filename="gtk_implementation/reports/relatorio_copia.html").write_pdf(
        "gtk_implementation/reports/" + archive_name + ".pdf",
        stylesheets=["gtk_implementation/reports/report_style.css"],
    )

    print(archive_name, "PDF has been created")
    store_report_address(
        "gtk_implementation/reports/" + archive_name + ".pdf", hora_emissao
    )
    try:
        os.remove("gtk_implementation/reports/relatorio_copia.html")
        os.remove("blacklist_graph.png")
        os.remove("whitelist_graph.png")

    except Exception as e:
        print(e)
