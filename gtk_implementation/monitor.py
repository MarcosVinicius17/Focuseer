import gi, psutil, time, json, threading

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from datetime import datetime

"""
1) usuario add o processo para uma das listas
2) o processo eh adicionado a uma lista
3) quando o usuario ativa um processo, verificar se ele faz parte de qual lista
4) dependendo de qual lista estiver, ir para whitelisted_data ou blacklisted_data

adiciona/remove_processo -> 

"""
whitelisted_processes = []
blacklisted_processes = []


def format_time(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def monitora_processo(process_name, data_type):
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"] == process_name:
            print("processo encontrado")
            start_time = time.time()
            while psutil.pid_exists(proc.info["pid"]):
                time.sleep(1)

            end_time = time.time()
            elapsed_time = int(end_time - start_time)

            # Load existing process data from JSON file
            try:
                with open("process_data.json", "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {
                    "day_data": {"date": "", "blacklist_data": {}, "whitelist_data": {}}
                }

            # Get the current date in DD/MM/YYYY format
            current_date = datetime.now().strftime("%d/%m/%Y")

            # Update or add the elapsed time for the process based on data_type
            if "date" in data["day_data"] and data["day_data"]["date"] == current_date:
                if data_type == 0:
                    print("Blacklist process")
                    data["day_data"]["blacklist_data"][process_name] = (
                        data["day_data"]["blacklist_data"].get(process_name, 0)
                        + elapsed_time
                    )
                elif data_type == 1:
                    print("whitelisted process")
                    data["day_data"]["whitelist_data"][process_name] = (
                        data["day_data"]["whitelist_data"].get(process_name, 0)
                        + elapsed_time
                    )
            else:
                data["day_data"]["date"] = current_date
                data["day_data"]["blacklist_data"] = (
                    {process_name: elapsed_time} if data_type == 0 else {}
                )
                data["day_data"]["whitelist_data"] = (
                    {process_name: elapsed_time} if data_type == 1 else {}
                )

            # Save updated process data to JSON file
            with open("process_data.json", "w") as f:
                json.dump(data, f, indent=4)

            print(f"The process '{process_name}' ran for {elapsed_time} seconds.")
            return elapsed_time

    # If the process is not running, return None
    print(f"The process '{process_name}' is not currently running.")
    return None


"""
Administra o status dos processos
"""


def update_process_to_monitor(process, status):
    """ver em qual list o processo esta"""
    if process in whitelisted_processes:
        print("whitelisted")
        if status == "checked":
            print("O processo", process, "esta ativo")
            threading.Thread(target=monitora_processo, args=(process, 1)).start()
    elif process in blacklisted_processes:
        print("blacklisted")
        if status == "checked":
            print("O processo", process, "esta ativo")
            threading.Thread(target=monitora_processo, args=(process, 0)).start()

    if status == "unchecked":
        print("O processo", process, "esta inativo")


"""
dialog para receber o nome do processo 
"""


def adiciona_processo(button, listbox):
    dialog = Gtk.Dialog(
        title="Adicionar processo",
        buttons=(
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,
        ),
    )
    dialog.set_default_size(200, 50)

    # Create a text entry field
    entry = Gtk.Entry()
    entry.set_text("Nome do processo")
    entry.set_activates_default(True)
    dialog.vbox.pack_start(entry, True, True, 0)
    entry.show()

    # Run the dialog and get the response
    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        text = entry.get_text()
        if listbox == 1:
            add_permitido(text)
            whitelisted_processes.append(text)
        if listbox == 2:
            add_nao_permitido(text)
            blacklisted_processes.append(text)
    dialog.destroy()


def remove_processo(button, listbox):
    # Create the dialog
    dialog = Gtk.Dialog(
        title="Remover processo",
        buttons=(
            Gtk.STOCK_OK,
            Gtk.ResponseType.OK,
        ),
    )
    dialog.set_default_size(200, 50)

    # Create a text entry field
    entry = Gtk.Entry()
    entry.set_text("Nome do processo")
    entry.set_activates_default(True)
    dialog.vbox.pack_start(entry, True, True, 0)
    entry.show()

    # Run the dialog and get the response
    response = dialog.run()

    if response == Gtk.ResponseType.OK:
        text = entry.get_text()
        if listbox == 1:
            remove_permitido(text)
        if listbox == 2:
            remove_nao_permitido(text)
    dialog.destroy()


def on_checkbox_toggled(checkbox):
    label = checkbox.get_label()
    status = "checked" if checkbox.get_active() else "unchecked"
    update_process_to_monitor(label, status)


def hide_label():
    lblAviso.hide()
    return False


def show_label():
    lblAviso.set_visible(True)
    GLib.timeout_add_seconds(2, hide_label)


def add_permitido(process):
    checkbox = Gtk.CheckButton(label=process)
    listPermitidos.add(checkbox)
    checkbox.connect("toggled", on_checkbox_toggled)
    checkbox.show_all()
    lblAviso.set_text(f"O processo " + process + " foi adicionado")
    show_label()


def add_nao_permitido(process):
    checkbox = Gtk.CheckButton(label=process)
    listNaoPermitidos.add(checkbox)
    checkbox.connect("toggled", on_checkbox_toggled)
    checkbox.show_all()
    lblAviso.set_text(f"O processo " + process + " foi adicionado")
    show_label()


def remove_permitido(process):
    children = listPermitidos.get_children()
    for child in children:
        if isinstance(child, Gtk.ListBoxRow):
            check_button = child.get_child()
            if isinstance(check_button, Gtk.CheckButton):
                label = check_button.get_label()
                if label == process:
                    lblAviso.set_text(f"O processo " + process + " foi removido")
                    show_label()
                    listPermitidos.remove(child)


def remove_nao_permitido(process):
    children = listNaoPermitidos.get_children()
    for child in children:
        if isinstance(child, Gtk.ListBoxRow):
            check_button = child.get_child()
            if isinstance(check_button, Gtk.CheckButton):
                label = check_button.get_label()
                if label == process:
                    lblAviso.set_text(f"O processo " + process + " foi removido")
                    show_label()
                    listNaoPermitidos.remove(child)


builder = Gtk.Builder()
builder.add_from_file("glade_screens/monitor.glade")

window = builder.get_object("window")
btnRemovePermitidos = builder.get_object("btnRemoverPermitidos")
btnRemoveNaoPermitidos = builder.get_object("btnRemoverNaoPerm")
listPermitidos = builder.get_object("listPermitidos")
listNaoPermitidos = builder.get_object("listNaoPermitidos")
btnAddPermitidos = builder.get_object("btnAddPermitidos")
btnAddNaoPermitidos = builder.get_object("btnAddNaoPermitidos")
lblAviso = builder.get_object("lblAviso")


btnAddPermitidos.connect("clicked", lambda btn: adiciona_processo(btn, 1))

btnAddNaoPermitidos.connect("clicked", lambda btn: adiciona_processo(btn, 2))

btnRemovePermitidos.connect("clicked", lambda btn: remove_processo(btn, 1))

btnRemoveNaoPermitidos.connect("clicked", lambda btn: remove_processo(btn, 2))


css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)

window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
btnRemovePermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

btnRemoveNaoPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

listPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

listNaoPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

btnAddNaoPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

btnAddPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window.show_all()
lblAviso.set_visible(False)
Gtk.main()
