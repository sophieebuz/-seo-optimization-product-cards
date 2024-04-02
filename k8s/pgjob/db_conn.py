import psycopg2


def local_conn() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host="seo-postgres-v2",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="password",
    )
