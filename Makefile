# Makefile for Quantum LMS Docker commands
# Usage: make <target>
# Windows: Install Make via chocolatey (choco install make) or use WSL

.PHONY: help build up down restart logs shell test clean prune

# Default target
help:
	@echo "Quantum LMS Docker Commands"
	@echo "============================"
	@echo ""
	@echo "  make build      - Build Docker image"
	@echo "  make up         - Start containers (foreground)"
	@echo "  make up-d       - Start containers (background)"
	@echo "  make down       - Stop and remove containers"
	@echo "  make restart    - Restart containers"
	@echo "  make logs       - View logs"
	@echo "  make logs-f     - Follow logs (real-time)"
	@echo "  make shell      - Enter container shell"
	@echo "  make test       - Run Manim test inside container"
	@echo "  make clean      - Stop containers and clean volumes"
	@echo "  make prune      - Remove all unused Docker resources"
	@echo ""

# Build the Docker image
build:
	@echo "Building Quantum LMS Docker image..."
	cd docker && docker-compose build

# Start containers (foreground)
up:
	@echo "Starting Quantum LMS..."
	cd docker && docker-compose up

# Start containers (background)
up-d:
	@echo "Starting Quantum LMS in background..."
	cd docker && docker-compose up -d
	@echo ""
	@echo "✅ Quantum LMS is running at http://127.0.0.1:5000"
	@echo "View logs: make logs-f"

# Stop containers
down:
	@echo "Stopping Quantum LMS..."
	cd docker && docker-compose down

# Restart containers
restart:
	@echo "Restarting Quantum LMS..."
	cd docker && docker-compose restart

# View logs
logs:
	cd docker && docker-compose logs

# Follow logs (real-time)
logs-f:
	cd docker && docker-compose logs -f

# Enter container shell
shell:
	@echo "Entering Quantum LMS container shell..."
	docker exec -it quantum-lms-app bash

# Run Manim test inside container
test:
	@echo "Running Manim test inside container..."
	docker exec quantum-lms-app python test_manim.py

# Stop and remove volumes (CAUTION: deletes database)
clean:
	@echo "⚠️  WARNING: This will delete the database!"
	@echo "Press Ctrl+C to cancel, or wait 5 seconds to continue..."
	@sleep 5
	cd docker && docker-compose down -v
	@echo "✅ Containers and volumes removed"

# Prune unused Docker resources
prune:
	@echo "Cleaning up unused Docker resources..."
	docker system prune -a
	@echo "✅ Cleanup complete"

# Build and start in one command
all: build up-d

# Development mode (with code sync)
dev:
	@echo "Starting in development mode..."
	@echo "Make sure to uncomment volume mount in docker-compose.yml"
	cd docker && docker-compose up

# Production build (no cache)
prod:
	@echo "Building for production (no cache)..."
	cd docker && docker-compose build --no-cache
	@echo "Starting in production mode..."
	cd docker && docker-compose up -d
