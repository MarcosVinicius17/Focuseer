import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def show_about_dialog(widget):
    about_dialog = Gtk.AboutDialog()

    # Set properties for the about dialog
    about_dialog.set_program_name("Focuseer")
    about_dialog.set_version("2.0")
    about_dialog.set_comments("Keep your productivity while working remotely")
    about_dialog.set_website("https://www.example.com")
    about_dialog.set_authors(["Marcos Vinícius"])
    about_dialog.set_logo_icon_name("my-application-icon")
    about_dialog.set_transient_for(widget.get_toplevel())

    style_provider_priority = 600
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), css_provider, style_provider_priority
    )

    context_about = about_dialog.get_style_context()

    context_about.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

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
