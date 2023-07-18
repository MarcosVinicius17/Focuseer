import gi, datetime, subprocess, sys
from pymongo import MongoClient

gi.require_version("Gtk", "3.0")
gi.require_version("GtkSource", "4")
from gi.repository import Gtk, Gdk, GtkSource, Pango


class Notes(Gtk.Application):
    sourceview = GtkSource.View()
    sourceview.set_show_line_numbers(True)
    sourceview.set_tab_width(4)
    sourceview.set_hexpand(True)
    sourceview.set_vexpand(True)
    font_desc = Pango.FontDescription("Monospace 12")
    sourceview.override_font(font_desc)

    def __init__(self):
        super().__init__()

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_default_size(400, 400)
        window.set_title("Focuseer")
        window.set_name("notes_window")

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

        delete_button = Gtk.EventBox()

        delete_image = Gtk.Image.new_from_file(
            "/home/marcos/Desktop/UNIP/tcc/nao_programacao/logos/icone_delete.png"
        )

        delete_button.add(delete_image)

        headerbar.pack_start(delete_button)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        scroll.add(Notes.sourceview)

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
        delete_button.connect("button-press-event", self.delete_note)

    def set_sourceview_text(self, text):
        print("inside the function")
        buffer = self.sourceview.get_buffer()
        buffer.set_text(text)

    """1st line will be the title"""

    def get_title(self):
        buffer = Notes.sourceview.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_iter_at_line(1)

        text = buffer.get_text(start_iter, end_iter, False).rstrip()

        return text

    def on_save_clicked(self, button, event):
        """
        MongoDB stuff
        """
        client = MongoClient()
        db = client.tcc_usuarios
        notes = db.notes

        """
        Getting the content
        """

        buffer = Notes.sourceview.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        note_content = buffer.get_text(start_iter, end_iter, False)
        titulo = self.get_title()

        """getting current time"""
        now = datetime.datetime.now()
        day = now.day
        month = now.strftime("%B")
        hour = now.hour
        minute = now.minute
        time_formatted = (
            str(day) + "/" + str(month) + "-" + str(hour) + ":" + str(minute)
        )

        """Insert or update note"""

        titulo = self.get_title()

        old_note = notes.find_one({"titulo": titulo})

        if old_note:
            note_update = notes.find_one_and_update(
                old_note, {"$set": {"texto": note_content, "hora": time_formatted}}
            )
        else:
            note_to_insert = {
                "titulo": titulo,
                "texto": note_content,
                "hora": time_formatted,
            }

            note_id = notes.insert_one(note_to_insert).inserted_id
            print("Insert successful, here is the user id: ", note_id)

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
        dialog.set_name("dialog")

        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            window = self.get_active_window()
            window.destroy()
        else:
            pass
        dialog.destroy()

    def delete_note(self, button, event):
        dialog = Gtk.MessageDialog(
            transient_for=self.get_active_window(),
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Tem certeza de que deseja apagar a nota?",
            title="Apagar nota",
        )

        dialog.set_default_size(300, 100)
        dialog.set_name("dialog")

        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            client = MongoClient()
            db = client.tcc_usuarios
            notes = db.notes

            title = self.get_title()

            delete_note = notes.delete_one({"titulo": title})

            dialog.destroy()

            print(delete_note.deleted_count, " document deleted.")

            window = self.sourceview.get_parent_window()
            if window:
                window.get_toplevel().destroy()

            subprocess.Popen([sys.executable, "gtk_implementation/notes_start.py"])

        else:
            dialog.destroy()


def create_application(title, text):
    app = Notes()
    app.set_sourceview_text(text)
    app.run(None)


if __name__ == "__main__":
    app = Notes()
    app.run(None)
