import sqlite3
con = sqlite3.connect('tg.db')


cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE callList
               (id INTEGER PRIMARY KEY)''')

cur.execute('''CREATE TABLE approver
               (id INTEGER PRIMARY KEY)''')

con.commit()
con.close()