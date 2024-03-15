import psycopg2
from utils.dataset import local_conn


def create_tables():
    try:
        with local_conn() as con:
            cursor = con.cursor()
            cursor.execute("CREATE SEQUENCE your_seq;")
            query = """CREATE TABLE \"images\" (
                       \"id\" INTEGER PRIMARY KEY default nextval('your_seq'),
                       \"category\" TEXT,
                       \"type\" TEXT,
                       \"name\" TEXT,
                       CONSTRAINT image_unique UNIQUE (category, type, name))"""
            cursor.execute(query)
    except:
        print("Table images are already exist")