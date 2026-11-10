import os
import psycopg


def db_connection():
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "5432")),
        dbname=os.environ.get("DB_NAME", "drt_lab"),
        user=os.environ.get("DB_USER", "drt_monitor"),
        password=os.environ["DB_PASSWORD"],
        connect_timeout=3,
        options="-c statement_timeout=5000 -c default_transaction_read_only=on",
        autocommit=True,
    )
