# Database Reliability Toolkit (DRT)

A reproducible PostgreSQL reliability engineering laboratory, with a Python/Flask REST API.

## Quickstart (Windows + Docker Desktop)

1. Install Docker Desktop (with WSL2 backend), Git and VS Code.
2. Copy the environment template: `Copy-Item .env.example .env`
3. Change both passwords in `.env` (do not commit this file).
4. Start the stack: `docker compose up --build -d`
5. Check status: `docker compose ps`
6. Test from PowerShell:
   - `Invoke-RestMethod http://localhost:8000/health/live`
   - `Invoke-RestMethod http://localhost:8000/health/ready`
   - `Invoke-RestMethod http://localhost:8000/api/v1/database/stats`
   - `Invoke-RestMethod http://localhost:8000/api/v1/database/size`
   - `Invoke-RestMethod http://localhost:8000/api/v1/orders/count`

The initial dataset contains 10,000 synthetic customers and 100,000 synthetic orders.
Postgres is exposed only on `127.0.0.1:5432` for local tools (DBeaver).

## Database access

DBeaver: host `localhost`, port `5432`, database `drt_lab`, username `drt_monitor`, password from `MONITOR_PASSWORD` in local `.env`.
The application uses the Docker Compose service hostname `db` instead of `localhost`.

## Development

Run `python -m pip install -r requirements-dev.txt`, `ruff check .`, `pytest -q` locally.

## Safety

Lab only; sample credentials in `.env.example` are placeholders. Do not expose the API or database to the internet. SQL data is synthetic. Runtime database connections use a restricted role and read-only sessions.

## Reset dataset (destructive)

`docker compose down -v` deletes the Postgres volume and all stored data. `docker compose up --build -d` initializes a new one. The scripts under `db/init` run only for a NEW database volume.

## Roadmap

- [x] PostgreSQL synthetic dataset and read-only diagnostic API
- [ ] Integration tests, structured errors, connection pooling, and API documentation
- [ ] Query metrics, blocking sessions and workload simulation
- [ ] Prometheus and Grafana
- [ ] Kubernetes and incident runbooks

## Known limitations

This is a learning MVP, not production-hardened. The Flask development server is used only for localhost laboratory testing. Replace it with a production WSGI server before deploying anywhere else. Pin dependencies and Docker images to tested versions/digests before promoting to CI/deployment environments. Current CI contains unit smoke tests, not database integration tests.
