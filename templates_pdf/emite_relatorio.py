from weasyprint import HTML
from jinja2 import Template
from datetime import datetime
import os


# Function to generate the PDF
def generate_pdf(data):
    # Load the Jinja2 environment and the HTML template
    env = Template(data)

    # Conteudo das variaveis
    nome = "admin"
    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y - %H:%M")
    archive_name = now.strftime("%d_%m_%Y_%H_%M")

    # Examples
    data_criacao = formatted_date
    hora_entrada = "08:30"
    hora_saida = "17:30"
    time_spent = "07:00"
    previous_time = "07:30"
    week_time_spent = "07:30"
    whitelist_graph = "/home/marcos/Desktop/UNIP/tcc/nao_programacao/logos/logo_v2.png"
    blacklist_graph = "/home/marcos/Desktop/UNIP/tcc/nao_programacao/logos/logo_v2.png"

    # Associa as variaveis
    html_out = env.render(
        nome=nome,
        data_criacao=data_criacao,
        hora_entrada=hora_entrada,
        hora_saida=hora_saida,
        time_spent=time_spent,
        previous_time=previous_time,
        week_time_spent=week_time_spent,
        whitelist_graph=whitelist_graph,
        blacklist_graph=blacklist_graph,
    )

    # Cria o PDF
    with open("relatorio.html", "w") as f:
        f.write(html_out)

    HTML(filename="relatorio.html").write_pdf(archive_name + ".pdf")
    print(archive_name, "PDF has been created")


# Example usage:
if __name__ == "__main__":
    # Load the template from the file
    with open("templates_pdf/relatorio.html", "r") as f:
        html_template = f.read()

    # Generate the PDF
    generate_pdf(html_template)
