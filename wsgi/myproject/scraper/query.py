import sqlite3

def getItems():
    #raw_input("Press Enter")
    conn=sqlite3.connect('database.db');
    c=conn.cursor()
    for i in c.execute('select * from item'):
        print (i)
    conn.close()
getItems()
