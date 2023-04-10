import gi, subprocess, sys, sqlite3, datetime


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def write_note(title, text, datetime):
    """Selecting the database"""
    conn = sqlite3.connect("/home/marcos/Desktop/UNIP/tcc/prototipos/user_notes.db")

    """Creating the table"""
    conn.execute("""CREATE TABLE notes (id INTEGER PRIMARY KEY, value TEXT)""")

    # Inserting the data
    conn.execute("INSERT INTO data (value) VALUES ('This is some data')")

    # Commit the changes
    conn.commit()


def get_note_info(button):

    """
    Getting the title
    """
    title_buffer = note_title.get_buffer()
    start, end = title_buffer.get_bounds()
    title = title_buffer.get_text(start, end, True)
    print(f"title:{title}")
    """
    Getting the text
    """
    text_buffer = note_text.get_buffer()
    start, end = text_buffer.get_bounds()
    text = text_buffer.get_text(start, end, True)
    print(f"text:{text}")

    """
    Getting the insertion time
    """
    """
    strftime para formatar a string fr forma adequada
    """
    # date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    write_note(title, text, date)


builder = Gtk.Builder()
builder.add_from_file("glade_screens/write_note.glade")
window = builder.get_object("Window")


note_title = builder.get_object("txtTitle")
note_text = builder.get_object("txtText")


btnWrite = builder.get_object("btnWrite")
btnWrite.connect("clicked", get_note_info)

window.show_all()

Gtk.main()
