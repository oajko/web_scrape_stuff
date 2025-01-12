import sqlite3

def create_db():
    con=sqlite3.connect('db1.db')
    cur=con.cursor()
    
    query='''CREATE TABLE IF NOT EXISTS urls(
    url TEXT,
    title TEXT
    )'''
    cur.execute(query)
    con.commit()
    con.close()


if __name__=='__main__':
    create_db()