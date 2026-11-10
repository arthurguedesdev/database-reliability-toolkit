#!/bin/sh
set -eu
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -v mon_pass="$MONITOR_PASSWORD" -v db_name="$POSTGRES_DB" <<'SQL'
SELECT format('CREATE ROLE drt_monitor LOGIN PASSWORD %L', :'mon_pass') \gexec
SELECT format('GRANT CONNECT ON DATABASE %I TO drt_monitor', :'db_name') \gexec
GRANT pg_read_all_stats TO drt_monitor;
GRANT USAGE ON SCHEMA public TO drt_monitor;
GRANT SELECT ON public.customers, public.orders TO drt_monitor;
SQL
