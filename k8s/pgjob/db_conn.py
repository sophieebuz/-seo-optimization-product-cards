import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

def local_conn() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host="seo-postgres-v2",
        port=5432,
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
    )
