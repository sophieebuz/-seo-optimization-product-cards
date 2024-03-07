import sqlite3

with sqlite3.connect('product_cards.db') as con:
    cursor = con.cursor()
    cursor.execute("SELECT * FROM images")
    print(cursor.fetchall())