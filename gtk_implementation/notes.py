import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GtkSource", "3.0")
from gi.repository import Gtk, Gdk, GtkSource, Pango


class MyApplication(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_default_size(400, 400)
        window.set_title("Focuseer")

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        window.add(main_box)

        # Create headerbar
        headerbar = Gtk.HeaderBar()
        headerbar.props.title = "Notas"
        main_box.pack_start(headerbar, False, False, 0)

        save_button = Gtk.EventBox()

        save_image = Gtk.Image.new_from_file(
            "/home/marcos/Desktop/UNIP/tcc/nao_programacao/logos/icone_save.png"
        )
        save_button.add(save_image)

        headerbar.pack_start(save_button)

        cancel_button = Gtk.EventBox()

        cancel_image = Gtk.Image.new_from_file(
            "/home/marcos/Desktop/UNIP/tcc/nao_programacao/logos/icone_abort.png"
        )
        cancel_button.add(cancel_image)

        headerbar.pack_start(cancel_button)

        sourceview = GtkSource.View()
        sourceview.set_show_line_numbers(True)
        sourceview.set_tab_width(4)
        sourceview.set_hexpand(True)
        sourceview.set_vexpand(True)

        font_desc = Pango.FontDescription("Monospace 12")
        sourceview.override_font(font_desc)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(sourceview)

        main_box.pack_start(scroll, True, True, 0)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(
            "/home/marcos/Desktop/UNIP/tcc/gtk_implementation/custom_colors.css"
        )

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self.add_window(window)
        window.show_all()

        save_button.connect("button-press-event", self.on_save_clicked)
        cancel_button.connect("button-press-event", self.on_cancel_clicked)

    def on_save_clicked(self, button, event):
        print("Save button clicked")

    def on_cancel_clicked(self, button, event):
        dialog = Gtk.MessageDialog(
            transient_for=self.get_active_window(),
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Tem certeza de que deseja sair?",
            title="Descartar nota",
        )

        dialog.set_default_size(300, 100)
        # dialog.get_style_context().add_class("dialog")
        dialog.set_name("dialog")

        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            print("Cancel button clicked - Yes")
        else:
            print("Cancel button clicked - No")
        dialog.destroy()


if __name__ == "__main__":
    app = MyApplication()
    app.run(None)
