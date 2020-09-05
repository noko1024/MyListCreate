import sqlite3
import os
import json

cwd = os.path.split(os.path.realpath(__file__))[0]
jsonPath = cwd + "/pivot.json"

conn = sqlite3.connect('niconico.db')
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS ids''')
c.execute('''DROP TABLE IF EXISTS ids_high''')
c.execute('''DROP TABLE IF EXISTS ids_low''')
c.execute("create table ids(id int,tag text,name text)")
c.execute("create table ids_high(id int,tag text)")
c.execute("create table ids_low(id int,tag text)")

data = {}

with open(jsonPath,mode="w") as f:
    json.dump(data,f,indent=4)

conn.commit()
conn.close()
