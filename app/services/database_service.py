from app.db import db_connection

def get_database_version():
    with db_connection() as conn:
        version = conn.execute(
            "SELECT current_setting('server_version')"
        ).fetchone()[0]

        return version

def get_database_connections():
    # 1. Abrir conexão com db_connection()
    with db_connection () as conn:
    # 2. Executar a consulta SQL em pg_stat_activity
        sessions = conn.execute(
           """
             SELECT
                state,
                COUNT(*) AS total_connections
            FROM pg_stat_activity
            WHERE datname = current_database()
            GROUP BY state
           """
        ).fetchall()
    # 3. Recuperar todas as linhas com fetchall()

    # 4. Transformar os resultados em um dicionário Python
        connections = {
            "active": 0,
            "idle:": 0,
            "idle in transaction": 0
        }
        for row in sessions:
            connections[row[0]] = row[1]

    return connections