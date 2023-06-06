from weasyprint import HTML
from jinja2 import Template
from datetime import datetime
import os

# Conteudo das variaveis
nome = "Marcos Vinícius F. Vieira"
now = datetime.now()
formatted_date = now.strftime("%d/%m/%Y - %H:%M")

data_criacao = formatted_date
hora_entrada = "08:30"
hora_saida = "17:30"


new_directory = "/home/marcos/Desktop/UNIP/tcc/templates_pdf"
os.chdir(new_directory)

with open("relatorio.html", "r") as f:
    html_template = Template(f.read())


# Associa as variaveis
html_out = html_template.render(
    nome=nome,
    data_criacao=data_criacao,
    hora_entrada=hora_entrada,
    hora_saida=hora_saida,
)

# Cria o PDF
HTML(string=html_out).write_pdf("output.pdf")
print("pdf criado")
