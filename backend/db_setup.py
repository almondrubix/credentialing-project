import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS responses (
          id INTEGER PRIMARY KEY,
          scenario TEXT,
          candidate_answer TEXT,
          baseline TEXT,
          uniqueness INTEGER,
          teamwork INTEGER,
          biz_savvy INTEGER,
          conscientiousness INTEGER
)
''')
conn.commit()
conn.close()

