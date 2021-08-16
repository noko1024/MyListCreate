import sqlite3


conn = sqlite3.connect('niconico.db')
c = conn.cursor()

c.execute("create table if not exists tableDB(tag txt primary key,tableName txt,mylistCount int,mylistName txt)")
c.execute("create table if not exists rmTable(id int primary key)")
c.execute("create table if not exists buffer(id int primary key,mylistNum int,tag txt)")

conn.commit()
conn.close()
