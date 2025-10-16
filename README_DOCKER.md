# Docker instructions for Credit Card Approval Predictor

This file explains how to build and run the application using Docker.

## Build the Docker image

```bash
# from repository root
docker build -t credit-card-approval:latest -f DockerFile .
```

## Run the container

```bash
docker run --rm -p 8000:8000 credit-card-approval:latest
```

The API will be available at `http://localhost:8000`. The FastAPI docs will be at `/docs`.

## Using docker-compose (development)

```bash
docker-compose up --build
```

This mounts the repository into the container for live edits. Remove the volume for production.

## Notes for deployment platforms

- Render: You can supply a Dockerfile in the repo and select the Docker environment when creating a new service.
- Heroku: Use container registry (but Render is preferred as discussed).

## Model files

If your `best_model.pkl` is large, consider storing it in an object store and downloading it at container start, or include it in the image explicitly depending on your security and size preferences.
