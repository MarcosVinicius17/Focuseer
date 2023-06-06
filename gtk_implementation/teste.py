import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

# Create a GtkWindow
window = Gtk.Window()
window.connect("destroy", Gtk.main_quit)

# Create a GtkImage widget
image = Gtk.Image.new_from_file("logos/logo_pequeno.png")

# Create an overlay widget
overlay = Gtk.Overlay()
window.add(overlay)

# Add the GtkImage widget to the overlay
overlay.add(image)

# Create a colored overlay widget
color_overlay = Gtk.DrawingArea()
color_overlay.set_size_request(
    800, 600
)  # Set the size of the overlay to match the image size
color_overlay.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1, 0, 0, 0.5))
overlay.add_overlay(color_overlay)

window.show_all()
Gtk.main()
