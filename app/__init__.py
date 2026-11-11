from flask import Flask, jsonify # type: ignore
import psycopg # type: ignore
from .db import db_connection
from .routes.health import health_bp
from .services.database_service import get_database_version


def create_app():
    app = Flask(__name__)

    app.register_blueprint(health_bp)

    """"
    @app.get("/health/live")
    def live():
        return jsonify(status="alive")
    """
    @app.get("/health/ready")
    def ready():
        try:
            with db_connection() as conn:
                conn.execute("SELECT 1").fetchone()
            return jsonify(status="ready")
        except psycopg.Error:
            return jsonify(status="unavailable"), 503

    @app.get("/api/v1/database/stats")
    def database_stats():
        try:
            with db_connection() as conn:
                row = conn.execute(
                    """SELECT datname, numbackends, xact_commit, xact_rollback,
                              blks_read, blks_hit, tup_returned, tup_fetched
                       FROM pg_stat_database WHERE datname = current_database()"""
                ).fetchone()
            return jsonify(dict(zip(("database", "connections", "commits", "rollbacks",
                                     "blocks_read", "blocks_hit", "tuples_returned",
                                     "tuples_fetched"), row)))
        except psycopg.Error:
            return jsonify(error="database_query_failed"), 503

    @app.get("/api/v1/database/size")
    def database_size():
        try:
            with db_connection() as conn:
                size = conn.execute("SELECT pg_database_size(current_database())").fetchone()[0]
            return jsonify(size_bytes=size)
        except psycopg.Error:
            return jsonify(error="database_query_failed"), 503

    @app.get("/api/v1/orders/count")
    def orders_count():
        try:
            with db_connection() as conn:
                total = conn.execute("SELECT count(*) FROM public.orders").fetchone()[0]
            return jsonify(orders=total)
        except psycopg.Error:
            return jsonify(error="database_query_failed"), 503

    """
    @app.get("/api/v1/database/version")
    def database_version():
        try:
            with db_connection() as conn:
                version = conn.execute ("SELECT current_setting('server_version')").fetchone()[0]
                return jsonify(version=version)
        except psycopg.Error:
            return jsonify(error="database_query_failed"), 503
    """

    @app.get("/api/v1/database/version")
    def database_version():
        try:
            version = get_database_version()
            return jsonify(version=version)
        except psycopg.Error:
            return jsonify(error="database_query_failed"), 503

    return app
