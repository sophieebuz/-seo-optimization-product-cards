from utils.dataset import local_conn

with local_conn() as con:
    cursor = con.cursor()
    cursor.execute("SELECT * FROM images")
    print(cursor.fetchall())