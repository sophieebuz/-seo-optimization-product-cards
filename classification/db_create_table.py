import sqlite3


def create_tables():
    try:
        with sqlite3.connect('product_cards.db') as con:
            cursor = con.cursor()
            query = """CREATE TABLE \"images\" (
                       \"id\" INTEGER PRIMARY KEY,
                       \"category\" TEXT,
                       \"type\" TEXT,
                       \"name\" TEXT,
                       CONSTRAINT image_unique UNIQUE (category, type, name))"""
            cursor.execute(query)
    except:
        print("Table images are already exist")