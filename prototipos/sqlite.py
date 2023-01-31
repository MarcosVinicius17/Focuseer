import sqlite3

# Connect to the database
conn = sqlite3.connect("/home/marcos/Desktop/UNIP/tcc/prototipos/data.db")

# Create a table
conn.execute("""CREATE TABLE data (id INTEGER PRIMARY KEY, value TEXT)""")

# Insert some data
conn.execute("INSERT INTO data (value) VALUES ('This is some data')")

# Commit the changes
conn.commit()


cursor = conn.execute("SELECT * FROM data")
for row in cursor:
    print(row)  # This will print "(1, 'This is some data')"

# Close the connection
conn.close()
