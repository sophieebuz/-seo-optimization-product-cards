from pathlib import Path

import psycopg2

print(Path.cwd() / "data" / "data")
# def local_conn() -> psycopg2.extensions.connection:
#     return psycopg2.connect(
#         host="localhost",
#         port=53320,
#         dbname="postgres",
#         user="postgres",
#     )
#
# with local_conn() as con:
#     cursor = con.cursor()
#     query = """CREATE TABLE \"images\" (
#                            \"id\" INTEGER PRIMARY KEY,
#                            \"category\" TEXT,
#                            \"type\" TEXT,
#                            \"name\" TEXT,
#                            CONSTRAINT image_unique UNIQUE (category, type, name))"""
#     cursor.execute(query)
#
#     cursor.execute("SELECT * FROM images")
#     print(cursor.fetchall())

