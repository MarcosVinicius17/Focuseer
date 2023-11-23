import gi, datetime, time, threading, sys, subprocess, json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from deepdiff import DeepDiff
import emite_relatorio


def end_day_message() -> None:
    dialog = Gtk.Dialog(
        "My Dialog", None, Gtk.DialogFlags.MODAL, ("Close", Gtk.ResponseType.OK)
    )
    dialog.set_default_size(200, 50)
    # Create a label
    label = Gtk.Label.new("label")

    # Add the label to the dialog's content area
    content_area = dialog.get_content_area()
    content_area.add(label)

    dialog.connect(
        "response",
        lambda dialog, response: dialog.destroy()
        if response == Gtk.ResponseType.OK
        else None,
    )
    dialog.show_all()
    Gtk.main()


def close_window() -> None:
    Gtk.quit()


def gerar_relatorio() -> None:
    with open("gtk_implementation/reports/report_with_pic.html", "r") as f:
        html_template = f.read()
    emite_relatorio.generate_pdf(html_template)


def open_monitor(button) -> None:
    subprocess.Popen([sys.executable, "gtk_implementation/monitor.py"])


def empty_json():
    with open("gtk_implementation/reports/data.json", "r") as file:
        data = json.load(file)

    def empty_recursive(obj):
        if isinstance(obj, dict):
            for key in obj:
                obj[key] = empty_recursive(obj[key])
        elif isinstance(obj, list):
            obj.clear()
        elif isinstance(obj, bool):
            obj = False
        else:
            obj = None
        return obj

    new_data = empty_recursive(data)

    with open("gtk_implementation/reports/data.json", "w") as file:
        json.dump(new_data, file, indent=4)
    # print("JSON esvaziado")


def encerrar_dia() -> None:
    total_de_items = 0
    itens_concluidos = 0
    itens_com_check = []
    unchecked = []

    """prepara o arquivo json"""
    with open("gtk_implementation/reports/data.json", "r") as file:
        data = json.load(file)

    """verifica quais objetivos foram concluidos"""
    for child in boxObjetivos.get_children():
        if isinstance(child, Gtk.CheckButton):
            total_de_items += 1
            if child.get_active():
                itens_concluidos += 1
                itens_com_check.append(child.get_label())
                data["objetivos_dia"]["checked"].append(child.get_label())
            else:
                unchecked.append(child.get_label())
                data["objetivos_dia"]["unchecked"].append(child.get_label())
    print(f"Concluidos:<> {itens_com_check}")
    print(f"Nao concluidos:<> {unchecked}")

    """
    erro
    """

    """calcula % de itens concluidos"""
    if total_de_items == 0:
        print("sem itens detectados")

        percentage = 0
    else:
        percentage = (itens_concluidos / total_de_items) * 100
        percentage_formatted = round(percentage, 2)
        data["objetivos_dia"]["completion_rate"] = percentage_formatted
        print("Taxa de conclusao:", percentage)
    with open("gtk_implementation/reports/data.json", "w") as file:
        json.dump(data, file, indent=4)
    print("gerando relatorio")
    gerar_relatorio()


def encerrar_dia_antes(button, yes_text="sim", no_text="Nao") -> None:
    dialog = Gtk.MessageDialog(
        None,
        0,  # Gtk.DialogFlags
        Gtk.MessageType.OTHER,
        Gtk.ButtonsType.YES_NO,
        "Isso irá encerrar as atividades do dia. \n\nTem certeza?",
    )

    dialog.set_title("Encerrar dia")

    dialog.set_default_size(200, 50)

    response = dialog.run()
    dialog.destroy()

    if response == Gtk.ResponseType.YES:
        encerrar_dia()
        #empty_json()
    elif response == Gtk.ResponseType.NO:
        return False


"""retorna a hora do encerramento"""


def get_hora_final() -> str:
    with open("gtk_implementation/reports/data.json", "r") as file:
        data = json.load(file)
        hora_final = data["hora_encerramento"]["hora"]
    return hora_final


def set_tempo_trabalho(window) -> None:
    """obtem hora atual no formato HH:MM"""
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M")
    """obtem o dia atual no formato DD/MM"""
    current_day = current_time.strftime("%d/%m")

    with open("gtk_implementation/reports/data.json", "r") as file:
        data = json.load(file)
        data["tempo_gasto_processos"]["date"]

    """le o data.json para obter a hora de encerramento"""
    hora_final = get_hora_final()
    """atualiza as labels"""
    lblInicio.set_text(formatted_time)
    lblFim.set_text(hora_final)
    """abre uma thread para atualizar o progresso"""
    update_thread = threading.Thread(target=update_progress)
    update_thread.start()


def update_progress() -> None:
    ending_time_text = lblFim.get_text()
    print(ending_time_text)
    try:
        ending_time_text = datetime.datetime.strptime(ending_time_text, "%H:%M").time()
        current_time = datetime.datetime.now().time()
        current_total_minutes = current_time.hour * 60 + current_time.minute
        ending_total_minutes = ending_time_text.hour * 60 + ending_time_text.minute
        total_minutes_difference = ending_total_minutes - current_total_minutes

        if total_minutes_difference <= 0:
            print("O tempo final esta no passado", ending_time_text)
            return

        print(f"Inicio: {current_time.strftime('%H:%M')}")
        print(f"Fim: {ending_time_text.strftime('%H:%M')}")

        while current_total_minutes < ending_total_minutes:
            current_time = datetime.datetime.now().time()
            current_total_minutes = current_time.hour * 60 + current_time.minute
            current_progress = (
                (
                    current_total_minutes
                    - (ending_total_minutes - total_minutes_difference)
                )
                / total_minutes_difference
                * 100
            )
            # print(f"Progress: {current_progress:.2f}%")
            progress = "{:.2f}%".format(current_progress)
            lblProgresso.set_text(str(progress))
            if current_progress == 100:
                print("Dia encerrado")
                end_day_message()
                encerrar_dia()
                break
            time.sleep(10)
    except ValueError:
        print("Formado inválido. Utilize o formato HH:MM.")


def ler_arquivo_json(arquivo):
    with open(arquivo, "r") as file:
        content = json.load(file)
    return content


def monitor_json_file():
    last_content = ler_arquivo_json("gtk_implementation/reports/data.json")

    while True:
        current_content = ler_arquivo_json("gtk_implementation/reports/data.json")

        if current_content != last_content:
            diff = DeepDiff(last_content, current_content)
            atualizar_pagina()
            last_content = current_content

        time.sleep(5)


# quando ha mudanca no json, apaga a GtkBox e as preenche novamente com os valores atualizados
def atualizar_pagina() -> None:
    processes_children = boxProcessos.get_children()
    time_children = boxTempo.get_children()

    for i in processes_children[1:]:
        boxProcessos.remove(i)
    for j in time_children[1:]:
        boxTempo.remove(j)
    monitor_tempo()
    monitor_processos()


def add_item_objetivos(button) -> None:
    dialog = Gtk.Dialog()
    dialog.set_title("Add Item to Box")
    dialog.set_transient_for(button.get_toplevel())

    text_entry = Gtk.Entry()
    text_entry.set_placeholder_text("Enter item text")

    content_area = dialog.get_content_area()
    content_area.add(text_entry)

    dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
    dialog.add_button("OK", Gtk.ResponseType.OK)
    dialog.set_default_response(Gtk.ResponseType.OK)

    dialog.show_all()

    response = dialog.run()
    if response == Gtk.ResponseType.OK:
        text = text_entry.get_text()

        # item nao pode ficar em branco
        if text == "":
            pass
        else:
            check_button = Gtk.CheckButton.new_with_label(text)

            # Temporarily remove the "Add Item" button
            boxObjetivos.remove(button)

            boxObjetivos.add(check_button)

            # Re-add the "Add Item" button at the end
            boxObjetivos.add(button)

            boxObjetivos.show_all()  # Show all items in the box

    dialog.destroy()


def monitor_processos() -> None:
    with open("gtk_implementation/reports/data.json", "r") as file:
        data = json.load(file)
        blacklist_data = data["monitor_data"]["blacklisted"]
        whitelist_data = data["monitor_data"]["whitelisted"]
        whitelist_label = Gtk.Label(label="Permitidos")
        boxProcessos.pack_start(whitelist_label, True, True, 0)
        whitelist_label.show()
        for j in whitelist_data:
            lbl = Gtk.Label(label=j)
            boxProcessos.pack_start(lbl, True, True, 0)
            lbl.show()
        blacklist_label = Gtk.Label(label="Não permitidos")
        boxProcessos.pack_start(blacklist_label, True, True, 0)
        blacklist_label.show()
        for i in blacklist_data:
            lbl = Gtk.Label(label=i)
            boxProcessos.pack_start(lbl, True, True, 0)
            lbl.show()
        whitelist_label.get_style_context().add_class("label_workscreen")
        blacklist_label.get_style_context().add_class("label_workscreen")
        whitelist_label.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        blacklist_label.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


def monitor_tempo() -> None:
    """
    1 - alarme
    """
    with open("gtk_implementation/reports/data.json", "r") as file:
        data = json.load(file)
        alarm_info = data["alarm_info"]

    if alarm_info["active"] == False:
        alarm_label = Gtk.Label(label="Nenhum alarme ativo")
        boxTempo.pack_start(alarm_label, True, True, 0)
        alarm_label.show()
    else:
        text_to_label = f"Alarme: {alarm_info['ring_time']}"
        alarm_label = Gtk.Label(label=text_to_label)
        boxTempo.pack_start(alarm_label, True, True, 0)
        alarm_label.show()

    alarm_label.get_style_context().add_class("label_workscreen")

    alarm_label.get_style_context().add_provider(
        css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    """
    2 - timer
    """
    timer_info = data["timer_info"]
    if timer_info["active_timer"] == False:
        timer_label = Gtk.Label(label="Nenhum timer ativo")
        boxTempo.pack_start(timer_label, True, True, 0)
        timer_label.show()
    else:
        text_to_label = f"Timer: {timer_info['timer_end']}"
        timer_label = Gtk.Label(label=text_to_label)
        boxTempo.pack_start(timer_label, True, True, 0)
        timer_label.show()

    timer_label.get_style_context().add_class("label_workscreen")

    timer_label.get_style_context().add_provider(
        css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    """
    3 - pomodoro
    """
    pomodoro_info = data["pomodoro_info"]
    if pomodoro_info["active_pomodoro"] == False:
        pomodoro_label = Gtk.Label(label="Nenhum pomodoro ativo")
        boxTempo.pack_start(pomodoro_label, True, True, 0)
        pomodoro_label.show()
    else:
        text_to_label = f"Status: {pomodoro_info['status']}"
        pomodoro_label = Gtk.Label(label=text_to_label)
        boxTempo.pack_start(pomodoro_label, True, True, 0)
        pomodoro_label.show()

    pomodoro_label.get_style_context().add_class("label_workscreen")

    pomodoro_label.get_style_context().add_provider(
        css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


def open_home(button) -> None:
    subprocess.Popen([sys.executable, "gtk_implementation/homepage.py"])


builder = Gtk.Builder()
builder.add_from_file("glade_screens/workscreen.glade")

window = builder.get_object("Window")

lblInicio = builder.get_object("lblInicio")
lblFim = builder.get_object("lblFim")
pgrBar = builder.get_object("pgrBar")
boxObjetivos = builder.get_object("boxObjetivos")
boxTempo = builder.get_object("boxTempo")
boxProcessos = builder.get_object("boxProcessos")
lblTempo = builder.get_object("lblTempo")
lblProcessos = builder.get_object("lblProcessos")
lblObjetivos = builder.get_object("lblObjetivos")
btnHome = builder.get_object("btnHome")
btnObjetivos = builder.get_object("btnObjetivos")
lblProgresso = builder.get_object("lblProgresso")
btnMonitor = builder.get_object("btnMonitor")

btnObjetivos.connect("clicked", add_item_objetivos)
window.connect("realize", set_tempo_trabalho)
btnHome.connect("clicked", open_home)
btnMonitor.connect("clicked", open_monitor)


btnEncerrar = builder.get_object("btnEncerrar")
btnEncerrar.connect("clicked", encerrar_dia_antes)

css_provider = Gtk.CssProvider()
css_provider.load_from_path("gtk_implementation/custom_colors.css")

window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

btnHome.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
if __name__ == "__main__":
    window.show_all()
    monitor_tempo()
    monitor_processos()
    my_thread = threading.Thread(target=monitor_json_file)
    my_thread.start()
    Gtk.main()
