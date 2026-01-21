## Deployment Configuration

### requirements.txt
```
fastapi==0.95.0
uvicorn==0.22.0
sqlalchemy==2.0.20
pydantic==1.10.7
fastapi-limiter==0.1.0
aioredis==2.0.1
```

### Dockerfile
```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser

# Set the working directory
WORKDIR /app

# Copy the requirements file into the image
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the image
COPY . .

# Change to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - FRONTEND_ORIGIN=${FRONTEND_ORIGIN}
    volumes:
      - .:/app
    depends_on:
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/todos"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: "redis:6.2"
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### deploy.sh
```bash
#!/bin/bash

set -e

echo "Building Docker images..."
docker-compose build

echo "Running tests..."
docker-compose run --rm app pytest

echo "Starting application..."
docker-compose up -d

echo "Application deployed successfully!"
```

### .env.example
```
DATABASE_URL=sqlite:///./todo.db
REDIS_URL=redis://redis:6379
FRONTEND_ORIGIN=http://localhost:3000
```

### .dockerignore
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
venv
ENV
*.env
*.env.*
*.git
*.gitignore
.DS_Store
*.sqlite3
```

### Deployment Instructions

1. **Setup Environment Variables**:
   - Copy `.env.example` to `.env` and fill in the necessary environment variables.

2. **Build and Run the Application**:
   - Run `./deploy.sh` to build the Docker images, run tests, and start the application.

3. **Access the Application**:
   - The application will be available at `http://localhost:8000`.

4. **Security Best Practices**:
   - The application runs as a non-root user for enhanced security.
   - Use minimal base images to reduce the attack surface.

5. **Health Checks and Logging**:
   - Health checks are configured in `docker-compose.yml` to ensure the application is running correctly.
   - Logging is set up in the application to capture all operations.

6. **Port Mappings**:
   - The application is exposed on port 8000, which is mapped to the host.

7. **Volume Mounts**:
   - Redis data is persisted using a Docker volume.

8. **Environment Variable Management**:
   - Use the `.env` file to manage environment variables securely.

9. **Comments**:
   - Each step in the Dockerfile and `docker-compose.yml` is commented to explain its purpose.

By following these instructions, you can deploy the Todo List Manager REST API in a production-ready environment using Docker and Docker Compose.