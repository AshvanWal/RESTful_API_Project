import sqlite3

conn = sqlite3.connect('talents.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE talent
          ''')

conn.commit()
conn.close()
