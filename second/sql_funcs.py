import sqlite3

def duplicates(path):
    conn=sqlite3.connect(path)
    cur=conn.cursor()
    query='''
        DELETE FROM scrappy_data
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM scrappy_data
            GROUP BY TITLE
            );
        '''
    cur.execute(query)
    conn.commit()
    conn.close()

def get_data(path):
    conn=sqlite3.connect(path)
    cur=conn.cursor()
    query='''
        SELECT * FROM scrappy_data
        '''
    cur.execute(query)
    data=cur.fetchall()
    conn.close()
    return data

def get_headers(path):
    conn=sqlite3.connect(path)
    cur=conn.cursor()
    cur.execute('PRAGMA table_info(scrappy_data)')
    data=cur.fetchall()
    conn.close()
    return data