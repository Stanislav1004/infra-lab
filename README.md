# Infra Lab

A learning project where I build production-style infrastructure around a small
notes API (Python + PostgreSQL). The application itself is intentionally simple:
the goal is everything around it, the way a DevOps engineer would set it up in a real team.

## Architecture

```
client -> Nginx (:8080) -> API (FastAPI, :8000, internal) -> PostgreSQL (:5432, internal)
```

- **Nginx** is the only public entry point. It proxies requests to the API and limits each client to 10 requests/s (burst 20); extra requests get `429`.
- **API** is not published to the host. It is reachable only through Nginx.
- **PostgreSQL** is not published to the host. Its data lives in a named volume (`pgdata`) and survives container restarts.
- Secrets live in `deploy/.env`, which is never committed.

## Prerequisites

- Git
- Docker with the Compose plugin

## Quick start

```bash
git clone https://github.com/Stanislav1004/infra-lab.git
cd infra-lab/deploy
cp .env.example .env
```

Open `deploy/.env` and replace `change-me` with a real password. It must be the same
in `POSTGRES_PASSWORD` and inside `DATABASE_URL`. A simple way to generate one:

```bash
openssl rand -hex 16
```

Start the stack:

```bash
docker compose up -d --build
docker compose ps
```

## Verify it works

```bash
curl localhost:8080/health    # {"status":"ok"}
curl localhost:8080/ready     # {"status":"ready"}  (database reachable)
curl localhost:8000/health    # connection refused: the API is not exposed directly
```

Interactive API docs: <http://localhost:8080/docs>. Try `POST /notes`, then `GET /notes`.

To see rate limiting in action:

```bash
for i in $(seq 1 40); do curl -s -o /dev/null -w "%{http_code}\n" localhost:8080/health; done
```

You should see `200` first and then `429`.

## Stop and clean up

```bash
docker compose down        # stop, keep the data
docker compose down -v     # stop and delete the database volume
```

## Troubleshooting

- `curl` fails right after `up`: the API needs a few seconds to start, wait and retry.
- `/ready` returns `503`: the database is not reachable; check `docker compose logs db`.
- API cannot connect after changing the password: the old password is stored in the volume. Run `docker compose down -v` and start again.

## Repository structure

- `app/` the FastAPI application, its `Dockerfile` and pinned `requirements.txt`
- `deploy/` `compose.yaml`, Nginx config in `nginx/`, `.env.example`
- `docs/` diagrams and notes

## Image security

The API image runs as a non-root user (UID 10001), has pinned dependencies,
and `pip` is removed from the final image. Python packages had 0 known
vulnerabilities in a Trivy scan; the Debian base image still reports findings
that come from `python:3.14.4-slim`.

## Status

Done: API, hardened Docker image, Compose stack with PostgreSQL, Nginx reverse proxy.

Next: CI/CD with GitHub Actions (lint, build, vulnerability scan, deploy), then
Ansible, Terraform, Kubernetes and monitoring.
