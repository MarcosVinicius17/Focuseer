import json
from datetime import datetime

filename = "/home/marcos/Desktop/UNIP/tcc/banco_dados.json"


def criarJson():
    data = {}
    data["notes"] = []
    with open("banco_dados.json", "w") as f:
        json.dump(data, f)
    print("json criado")


def escreverJson(titulo, texto):
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(filename, "r") as fp:
        info = json.load(fp)
    info["notes"].append({"titulo": titulo, "texto": texto, "hora": current_time})

    with open(filename, "w") as fp:
        json.dump(info, fp)
    print("finished")


def listarJson():
    titulos = []
    textos = []
    horas = []
    v = 1
    try:
        with open(filename) as json_file:
            if v == 0:
                print("Arquivo em branco")
            else:
                data = json.load(json_file)
                for p in data["notes"]:
                    textos.append(p["texto"])
                    titulos.append(p["titulo"])
                    horas.append(p["hora"])

                return (titulos, textos, horas)
    except FileNotFoundError:
        print("Arquivo nao localizado.")


def procura_nota(titulo):
    extensoesDoConjunto = []

    with open(filename) as json_file:
        data = json.load(json_file)
        for i in data["notes"]:
            extensoes1 = []
            if i["titulo"] == titulo:
                print(f"encontrado:", i["titulo"])

                # return extensoesDoConjunto


# procura_nota("xxxxx")

escreverJson("teste", "heheheh dasdad dasdad")
