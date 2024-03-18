import psycopg2
from utils.dataset import local_conn


def create_tables():
    try:
        with local_conn() as con:
            cursor = con.cursor()
            cursor.execute("CREATE SEQUENCE seo_seq;")
            query = """CREATE TABLE \"images\" (
                       \"id\" INTEGER PRIMARY KEY default nextval('seo_seq'),
                       \"category\" TEXT,
                       \"type\" TEXT,
                       \"name\" TEXT,
                       CONSTRAINT image_unique UNIQUE (category, type, name))"""
            cursor.execute(query)
        print("Table images and seo_seq CREATED!")
    except:
        print("Table images are already exist")

    try:
        with local_conn() as con:
            cursor = con.cursor()
            cursor.execute("CREATE SEQUENCE celery_seq;")
            query = """CREATE TABLE \"celery_training_status\" (
                       \"id\" INTEGER PRIMARY KEY,
                       \"task_id\" VARCHAR(155),
                       \"status\" VARCHAR(50),
                       CONSTRAINT task_id_unique UNIQUE (task_id))"""
            cursor.execute(query)
        print("Table celery_training_status and celery_seq CREATED!")
    except:
        print("Table celery_training_status are already exist")

create_tables()