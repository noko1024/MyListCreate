import sqlite3


conn = sqlite3.connect('niconico.db')
c = conn.cursor()

c.execute("create table if not exists tableDB(mylistName txt primary key,tableName txt,mylistCount int)")
c.execute("create table if not exists rmTable(id int primary key)")
c.execute("create table if not exists buffer(id int primary key,mylistNum int,mylistName txt)")

conn.commit()
conn.close()
