import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


import estruturas

"""
6/8
ver como ira implementar as boxes para tempo (alarme, timer e pomodoro) e o monitor de processos
"""


# atualiza a pagina em um certo intervalo de tempo para ver se ha algum update
def atualizar_pagina() -> None:
    pass


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
        check_button = Gtk.CheckButton.new_with_label(text)

        # Temporarily remove the "Add Item" button
        boxObjetivos.remove(button)

        # Add the new check button
        boxObjetivos.add(check_button)

        # Re-add the "Add Item" button at the end
        boxObjetivos.add(button)

        boxObjetivos.show_all()  # Show all items in the box

    dialog.destroy()


def add_item_processos() -> None:
    pass


def add_item_tempo() -> None:
    """
    1 - alarme
    """
    alarm_exists = estruturas.alarm_info
    if alarm_exists["active_alarm"] == False:
        new_label = Gtk.Label("Nao ha alarme ativo")
        boxTempo.pack_start(new_label, True, True, 0)
        new_label.show()
    else:
        # print(f"Alarme programado para {alarm_exists['ring_time']}")
        text_to_label = f"Alarme: {alarm_exists['ring_time']}"
        new_label = Gtk.Label(text_to_label)
        boxTempo.pack_start(new_label, True, True, 0)
        new_label.show()
    """
    2 - timer
    """
    timer_exists = estruturas.timer_info
    if timer_exists["active_timer"] == False:
        new_label = Gtk.Label("Nao ha timer ativo")
        boxTempo.pack_start(new_label, True, True, 0)
        new_label.show()
    else:
        text_to_label = f"Timer: {timer_exists['timer_end']}"
        new_label = Gtk.Label(text_to_label)
        boxTempo.pack_start(new_label, True, True, 0)
        new_label.show()
    """
    3 - pomodoro
    """
    pomodoro_exists = estruturas.pomodoro_info
    if pomodoro_exists["active_pomodoro"] == False:
        new_label = Gtk.Label("Nao ha pomodoro ativo")
        boxTempo.pack_start(new_label, True, True, 0)
        new_label.show()
    else:
        text_to_label = f"Status do pomodoro: {pomodoro_exists['status']}"
        new_label = Gtk.Label(text_to_label)
        boxTempo.pack_start(new_label, True, True, 0)
        new_label.show()


def set_tempo_trabalho(inicio, fim) -> None:
    lblInicio.set_text(inicio)
    lblFim.set_text(fim)


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

btnObjetivos.connect("clicked", add_item_objetivos)


css_provider = Gtk.CssProvider()
css_provider.load_from_path("gtk_implementation/custom_colors.css")

window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

btnHome.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window.show_all()
# exemplo
# set_tempo_trabalho("06:00", "12:00")
add_item_tempo()
Gtk.main()
