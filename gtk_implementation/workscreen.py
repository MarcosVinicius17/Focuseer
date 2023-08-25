import gi, datetime, time, threading, sys, subprocess, json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from deepdiff import DeepDiff

"""
https://pypi.org/project/tqdm/
barra de progresso
"""


def esvaziar_json():
    with open("gtk_implementation/temp_data.json", "r") as file:
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

    with open("gtk_implementation/temp_data.json", "w") as file:
        json.dump(new_data, file, indent=4)


"""
1) obter data dos processos (tempo gasto)
2) gerar relatório (passar valores para o .py responsavel)
"""


def encerrar_dia(button) -> None:
    total_items = 0
    checked_items = 0
    checked = []
    unchecked = []

    with open("gtk_implementation/temp_data.json", "r") as file:
        data = json.load(file)

    for child in boxObjetivos.get_children():
        if isinstance(child, Gtk.CheckButton):
            total_items += 1
            if child.get_active():
                checked_items += 1
                checked.append(child.get_label())
                data["objetivos_dia"]["checked"].append(child.get_label())
            else:
                unchecked.append(child.get_label())
                data["objetivos_dia"]["unchecked"].append(child.get_label())
    print(f"checked: {checked}")
    print(f"unchecked: {unchecked}")

    if total_items == 0:
        return 0.0
    else:
        percentage = (checked_items / total_items) * 100
        data["objetivos_dia"]["completion_rate"] = percentage
        print("completion:", percentage)
    with open("gtk_implementation/temp_data.json", "w") as file:
        json.dump(data, file, indent=4)


def get_hora_final() -> str:
    with open("gtk_implementation/temp_data.json", "r") as file:
        data = json.load(file)
        hora_final = data["hora_encerramento"]["hora"]
    return hora_final


def set_tempo_trabalho(window) -> None:
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M")
    hora_final = get_hora_final()
    lblInicio.set_text(formatted_time)
    lblFim.set_text(hora_final)
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
            print("The target time is in the past", ending_time_text)
            return

        print(f"Start time: {current_time.strftime('%H:%M')}")
        print(f"End time: {ending_time_text.strftime('%H:%M')}")

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
            print(f"Progress: {current_progress:.2f}%")
            lblProgresso.set_text(str(current_progress) + "%")
            if current_progress == 100:
                break
            time.sleep(10)
    except ValueError:
        print("Invalid time format. Please use HH:MM.")


def ler_arquivo_json(arquivo):
    with open(arquivo, "r") as file:
        content = json.load(file)
    return content


def monitor_json_file():
    last_content = ler_arquivo_json("gtk_implementation/temp_data.json")

    while True:
        current_content = ler_arquivo_json("gtk_implementation/temp_data.json")

        if current_content != last_content:
            diff = DeepDiff(last_content, current_content)
            atualizar_pagina()
            last_content = current_content

        time.sleep(10)


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
    with open("gtk_implementation/temp_data.json", "r") as file:
        data = json.load(file)
        blacklist_data = data["monitor_data"]["blacklisted"]
        whitelist_data = data["monitor_data"]["whitelisted"]
        whitelist_label = Gtk.Label(label="Whitelist")
        boxProcessos.pack_start(whitelist_label, True, True, 0)
        whitelist_label.show()
        for j in whitelist_data:
            lbl = Gtk.Label(label=j)
            boxProcessos.pack_start(lbl, True, True, 0)
            lbl.show()
        blacklist_label = Gtk.Label(label="Blacklist")
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
    with open("gtk_implementation/temp_data.json", "r") as file:
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

btnObjetivos.connect("clicked", add_item_objetivos)
window.connect("realize", set_tempo_trabalho)
btnHome.connect("clicked", open_home)


btnEncerrar = builder.get_object("btnEncerrar")
btnEncerrar.connect("clicked", encerrar_dia)

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
    # set_tempo_trabalho(window, "00:00", "00:00")
    Gtk.main()
