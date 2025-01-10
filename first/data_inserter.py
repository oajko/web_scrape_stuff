import sqlite3

def insert_data(url,title):
    con=sqlite3.connect('init_start/db1.db')
    cur=con.cursor()
    query="""INSERT INTO urls VALUES
    (?,?)
    """
    cur.execute(query,(url,title))
    con.commit()
    con.close()
