import sqlite3

def create_db():
    path='more_advanced/scrapydb.db'
    con=sqlite3.connect(path)
    cur=con.cursor()
    query='''
        CREATE TABLE IF NOT EXISTS scrappy_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        developer TEXT,
        players TEXT,
        description TEXT,
        price FLOAT,
        currency TEXT,
        stock TEXT,
        genres TEXT,
        stars INT,
        platform TEXT,
        related_titles TEXT,
        image TEXT
    )'''

    cur.execute(query)
    con.commit()
    con.close()
    print('created!')


if __name__=='__main__':
    create_db()