import sqlite3

conn = sqlite3.connect('talents.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE talent
          (id INTEGER PRIMARY KEY ASC, 
           first_name VARCHAR(250) NOT NULL,
           last_name VARCHAR(250) NOT NULL,
           talent_num VARCHAR(100) NOT NULL,
           date_debut VARCHAR(100) NOT NULL,
           type VARCHAR(10) NOT NULL,
           award_num INTEGER,
           movie_list VARCHAR (100),
           model_type VARCHAR(20)
           )
          ''')

conn.commit()
conn.close()
