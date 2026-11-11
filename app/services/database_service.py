from app.db import db_connection

def get_database_version():
    with db_connection() as conn:
        version = conn.execute(
            "SELECT current_setting('server_version')"
        ).fetchone()[0]

        return version