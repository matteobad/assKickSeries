import sqlite3
import zlib
import requests
import os


API = 'https://kickass.so/hourlydump.txt.gz'
SERIES_URL = 'https://kickass.so/serie-tv'


# Aggiorna file API
def updateAPI():
    response = requests.get(API)
    data = zlib.decompress(response.content, zlib.MAX_WBITS | 16)

    with open('hourlydump.txt', 'wb') as file:
        file.write(data)
        file.close()


# Aggiorna database serie TV
def updateDb():
    con = sqlite3.connect('database.db')
    cursor = con.cursor()

    cursor.execute('DROP TABLE IF EXISTS serieTV;')
    cursor.execute('CREATE TABLE serieTV (id integer primary key, name text, page text)')
    con.commit()

    for i in range (1, 46000):
        page = ''.join(SERIES_URL+str(i))
        source = estract.estractSource(page)
        name = estract.estractName(source)
        if name:
            print(i, name)
            cursor.execute('INSERT INTO serieTV (name, page) VALUES (?, ?)', (name, page))

    con.commit()
    con.close()
    os.system("pause")

