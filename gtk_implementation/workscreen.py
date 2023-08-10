import gi, datetime, time, threading, sys, subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


import estruturas


def set_tempo_trabalho(window, inicio, fim) -> None:
    lblInicio.set_text(inicio)
    lblFim.set_text(fim)
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

        # item nao pode ficar em branco
        if text == "":
            pass
        else:
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
    processes_list = estruturas.monitor_data


def add_item_tempo() -> None:
    """
    1 - alarme
    """
    alarm_exists = estruturas.alarm_info
    if alarm_exists["active_alarm"] == False:
        alarm_label = Gtk.Label(label="Nao ha alarme ativo")
        boxTempo.pack_start(alarm_label, True, True, 0)
        alarm_label.show()
    else:
        # print(f"Alarme programado para {alarm_exists['ring_time']}")
        text_to_label = f"Alarme: {alarm_exists['ring_time']}"
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
    timer_exists = estruturas.timer_info
    if timer_exists["active_timer"] == False:
        timer_label = Gtk.Label(label="Nao ha timer ativo")
        boxTempo.pack_start(timer_label, True, True, 0)
        timer_label.show()
    else:
        text_to_label = f"Timer: {timer_exists['timer_end']}"
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
    pomodoro_exists = estruturas.pomodoro_info
    if pomodoro_exists["active_pomodoro"] == False:
        pomodoro_label = Gtk.Label(label="Nao ha pomodoro ativo")
        boxTempo.pack_start(pomodoro_label, True, True, 0)
        pomodoro_label.show()
    else:
        text_to_label = f"Status do pomodoro: {pomodoro_exists['status']}"
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
window.connect("realize", set_tempo_trabalho, "17:00", "16:51")
btnHome.connect("clicked", open_home)

css_provider = Gtk.CssProvider()
css_provider.load_from_path("gtk_implementation/custom_colors.css")

window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

btnHome.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window.show_all()
add_item_tempo()
Gtk.main()
