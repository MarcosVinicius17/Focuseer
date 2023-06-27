import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def button_clicked(widget):
    print("Button clicked!")


def main():
    # Create a new Gtk.Window
    window = Gtk.Window()
    window.set_default_size(200, 200)
    window.connect("destroy", Gtk.main_quit)

    # Create a Gtk.Button
    button = Gtk.Button()
    window.add(button)

    # Create a Gtk.Image
    image = Gtk.Image()
    image.set_from_file(
        "/home/marcos/Desktop/UNIP/tcc/nao_programacao/logos/icone_alarme.png"
    )

    # Set the image as the label of the button
    button.set_image(image)

    # Connect the "clicked" signal of the button to the button_clicked function
    button.connect("clicked", button_clicked)

    # Show all the widgets
    window.show_all()

    # Start the Gtk main loop
    Gtk.main()


if __name__ == "__main__":
    main()
