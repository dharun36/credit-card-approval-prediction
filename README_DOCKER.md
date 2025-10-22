# Docker + Render deployment guide

This project runs a FastAPI app for credit card approval predictions. Below are copy‑ready steps to run it locally with Docker and deploy it to Render using the existing `DockerFile`.

## Local: build and run with Docker

```powershell
# From repo root
docker build -t credit-card-approval:latest -f Dockerfile .
docker run --rm -p 8000:8000 credit-card-approval:latest
```

Open http://localhost:8000 for the app and http://localhost:8000/docs for the API docs.

Notes
- The image runs `uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}` so it binds to port 8000 locally and to the `PORT` env var in cloud.
- If your model files are large, see the “Model files” section below.

## Local: docker-compose for development

```powershell
docker-compose up --build
```

What this does
- Builds the same image using `Dockerfile`.
- Mounts the project directory into `/app` for live reloading.
- Runs `uvicorn` with `--reload` on port 8000.

Stop with Ctrl+C, or in another terminal:

```powershell
docker-compose down
```

## Deploy to Render (Docker Web Service)

Prerequisites
- Your repo is pushed to GitHub (this repo already contains `DockerFile`).

Steps
1. In the Render dashboard, click New > Web Service.
2. Connect your GitHub account and select the repository.
3. Select the branch to deploy (e.g., `dockerize` or `main`).
4. Runtime: choose Docker.
5. Root directory: `/` (repo root).
6. Dockerfile path: `Dockerfile` (standard Docker naming).
7. Auto Deploy: enable if you want every push to deploy.
8. Instance type: choose Free (for testing) or a paid plan.
9. Click Create Web Service.

Render specifics
- Port: Render sets an environment variable `PORT` (commonly 10000). Our image uses `--port ${PORT:-8000}`, so it will bind correctly on Render without extra config.
- Health: Once deployed, Render will show your service URL. Your FastAPI docs will be at `/docs`.

Optional settings
- Environment variables: Add any secrets or config here. None are required by default for this app.
- Build / Start commands: Leave empty for Docker services; the Dockerfile defines them.
- Auto-scaling: Configure as needed.

## Model files

This repo already includes `best_model.pkl`. The app tries to load `scaler.pkl` too; if it’s missing, a default StandardScaler is used (you’ll see a warning in logs). If you want to use a custom scaler:
- Add `scaler.pkl` to the repo (kept small), or
- Download it at container start (e.g., from cloud storage) in an entrypoint script, or
- Mount it with a volume for local dev: `-v ${PWD}:/app`.

## Quick commands

```powershell
# Build
docker build -t credit-card-approval:latest -f Dockerfile .

# Run
docker run --rm -p 8000:8000 credit-card-approval:latest

# Logs (follow)
docker logs -f <container_id>

# Stop all
docker stop $(docker ps -q)
```
