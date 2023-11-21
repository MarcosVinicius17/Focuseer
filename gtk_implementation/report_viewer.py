import gi, os, subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from pymongo import MongoClient


def open_pdf(pdf_file_path) -> None:
    # Get the current working directory
    current_directory = os.getcwd()

    # Construct the absolute path to the PDF file
    absolute_path = os.path.join(current_directory, pdf_file_path)

    # Check if the file exists
    if os.path.exists(absolute_path):
        subprocess.run(["open", absolute_path], check=True)
    else:
        print(f"Arquivo nao encontrado: {absolute_path}")


def load_addresses(window) -> None:
    client = MongoClient()
    db = client.tcc_usuarios
    reports = db.reports

    cursor = reports.find({}, {"_id": 0, "endereco": 1, "data_emissao": 1})

    values_list = []

    # Iterate through the cursor and append values to the list
    for entry in cursor:
        values_list.append(
            {"endereco": entry["endereco"], "data_emissao": entry["data_emissao"]}
        )

    # Close the MongoDB connection
    client.close()

    # Print the collected values at the end
    for values in values_list:
        print(f"Address: {values['endereco']}, Hour: {values['data_emissao']}")
        label_text = f"Relatório do dia {values['data_emissao']}"
        link_button = Gtk.LinkButton.new_with_label("Abrir relatório", label_text)
        listbox_obj.add(link_button)
        link_button.connect(
            "activate-link",
            lambda button: open_pdf("gtk_implementation/reports/20_11_2023_19_35.pdf"),
        )

        link_button.show_all()


builder = Gtk.Builder()
builder.add_from_file("glade_screens/relatorios.glade")

window = builder.get_object("Window")

listbox_obj = builder.get_object("listBox")

css_provider = Gtk.CssProvider()

css_provider.load_from_path("gtk_implementation/custom_colors.css")

window.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

listbox_obj.get_style_context().add_provider(
    css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window.connect("realize", load_addresses)
window.show_all()

# load_addresses()
Gtk.main()
