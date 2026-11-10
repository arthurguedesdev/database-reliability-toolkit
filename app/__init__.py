from flask import Flask, jsonify
import psycopg
from .db import db_connection


def create_app():
    app = Flask(__name__)

    @app.get("/health/live")
    def live():
        return jsonify(status="alive")

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

    return app
