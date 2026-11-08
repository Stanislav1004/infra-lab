# Infra Lab

A learning project where I build production-style infrastructure around a small
notes API (Python + PostgreSQL). The application itself is intentionally simple:
the goal is everything around it, the way a DevOps engineer would set it up in a real team.

## What this project covers

- Containerization: Docker, multi-stage builds, Docker Compose
- Reverse proxy: Nginx with rate limiting
- CI/CD: GitHub Actions (lint, build, vulnerability scan, deploy)
- Infrastructure as Code: Ansible, Terraform
- Orchestration: Kubernetes (k3s), Helm, ArgoCD
- Observability: Prometheus, Grafana, Loki
- Security: secrets management, non-root containers, image scanning

## Repository structure

- `app/` application code and its Dockerfile.
- `deploy/` Compose files, Nginx configs, later Ansible, Terraform and Kubernetes manifests.
- `docs/` diagrams and notes.

## Prerequisites

- Git
- Docker

## Status

Work in progress. Currently: project skeleton.

## Quick start

Coming soon.
