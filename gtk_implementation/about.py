import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def show_about_dialog(widget):
    about_dialog = Gtk.AboutDialog()

    # Set properties for the about dialog
    about_dialog.set_program_name("Focuseer")
    about_dialog.set_version("1.0")
    about_dialog.set_comments("Keep your productivity while working remotely")
    about_dialog.set_website("https://www.example.com")
    about_dialog.set_authors(["Marcos Vinícius"])
    about_dialog.set_logo_icon_name("my-application-icon")
    about_dialog.set_transient_for(widget.get_toplevel())

    # Run the dialog
    about_dialog.run()
    about_dialog.destroy()


window = Gtk.Window()
menu_bar = Gtk.MenuBar()

# Create the "About" menu item
about_menu_item = Gtk.MenuItem(label="About")
about_menu_item.connect("activate", show_about_dialog)

# Add the "About" menu item to the menu bar
menu_bar.append(about_menu_item)

window.add(menu_bar)
window.show_all()

Gtk.main()
