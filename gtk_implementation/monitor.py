import gi, psutil, time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


def format_time(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


"""
1 - Verificar como pausar o processo
1.1 - Talvez salvar em um json contendo o nome do processo e o tempo. 
Quando o processo for selecionado, verificar se ele consta no json. Se sim, obter o tempo e soma-lo.
Descartar o json no final do dia

"""


def monitora_processo(process):
    # Check if the process is already running
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == process:
            print(f"Process '{process}' is already running.")
            break
    else:
        print(f"Process '{process}' is not running.")
        return

    # Process is running, start the stopwatch
    start_time = time.time()
    print("Stopwatch started.")

    # Check if the process is still running in a loop
    while True:
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] == process:
                # Process is still running, continue the loop
                break
        else:
            # Process is no longer running, stop the stopwatch
            end_time = time.time()
            elapsed_time = end_time - start_time
            elapsed_formatted = format_time(elapsed_time)
            print(f"Process '{process}' stopped. Elapsed time: {elapsed_formatted}")
            break
        time.sleep(1)  # Wait for 1 second before checking again


"""
Administra o status dos processos
"""


def update_process_to_monitor(process, status):
    if status == "checked":
        print("O processo", process, "esta ativo")
        monitora_processo(process)

    if status == "unchecked":
        print("O processo", process, "esta inativo")


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
        if listbox == 2:
            add_nao_permitido(text)
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


"""
CSS
"""

css_provider = Gtk.CssProvider()
css_provider.load_from_path(
    "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
)

context_window = window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnPermitidos = btnRemovePermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
context_btnRemoveNaoPermitidos = (
    btnRemoveNaoPermitidos.get_style_context().add_provider(
        css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
)
context_listPermitidos = listPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

context_listNaoPermitidos = listNaoPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

context_btnAttNaoPermitidos = btnAddNaoPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

context_btnAttPermitidos = btnAddPermitidos.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
"""
END CSS
"""

# add_nao_permitido("steam")
# add_permitido("VSCode")
# add_permitido("Teams")
# add_nao_permitido("Spotify")


window.show_all()
# window_show_all() coloca todos os widgets como visiveis
lblAviso.set_visible(False)
Gtk.main()
