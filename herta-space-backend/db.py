import sqlite3

cxn = sqlite3.connect('credentials.db')
cursor = cxn.cursor()
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              email TEXT UNIQUE,
              password_hash VARCHAR(128))''')
cxn.commit()
cxn.close()