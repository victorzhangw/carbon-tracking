# Deployment Directory

## Purpose

This directory contains deployment configuration files for various platforms and services.

## Contents

- `render.yaml` - Render.com deployment configuration
- `Dockerfile.voice-api` - Docker configuration for voice API service
- `nginx-voice.conf` - Nginx configuration for voice service proxy

## Usage

### Render Deployment

The `render.yaml` file defines services for Render.com platform deployment:

```bash
# Deploy to Render (automatic when pushed to connected repository)
git push origin main
```

### Docker Deployment

Build and run the voice API service:

```bash
# Build Docker image
docker build -f config/deployment/Dockerfile.voice-api -t voice-api .

# Run container
docker run -p 8000:8000 voice-api
```

### Nginx Configuration

Copy the nginx configuration to your nginx sites directory:

```bash
# Copy configuration
sudo cp config/deployment/nginx-voice.conf /etc/nginx/sites-available/voice-api

# Enable site
sudo ln -s /etc/nginx/sites-available/voice-api /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

## Related Directories

- `/config/requirements/` - Dependency files referenced in deployment configs
- `/docs/guides/` - Deployment guides and documentation
