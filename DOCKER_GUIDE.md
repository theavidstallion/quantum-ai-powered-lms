# 🐳 Docker Deployment Guide for Quantum LMS

Complete guide for running Quantum LMS in Docker containers with all dependencies pre-installed.

## 🎯 What You Get

✅ **One-command deployment** - Everything installs automatically  
✅ **All dependencies included** - Python 3.12, FFmpeg, Manim CE, LaTeX  
✅ **Isolated environment** - No conflicts with your system  
✅ **Cross-platform** - Works on Windows, macOS, Linux  
✅ **Production-ready** - Health checks, resource limits, volume persistence  

## 📋 Prerequisites

### Install Docker Desktop
**Windows/macOS**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)

**Linux**:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER  # Add user to docker group
```

### Verify Installation
```bash
docker --version  # Should show Docker version 24.0+
docker-compose --version  # Should show version 2.20+
```

## 🚀 Quick Start (30 seconds)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/quantum-lms.git
cd quantum-lms/Quantum-
```

### Step 2: Launch Container (Environment already configured)
```bash
cd docker
docker-compose up --build
```

**That's it!** Access at **http://127.0.0.1:5000** 🎉

---

## 📖 Detailed Instructions

### Option A: Docker Compose (Recommended)

**Advantages**: One command, automatic networking, volume management, health checks

```bash
# Navigate to docker folder
cd e:\Projects\quantum-lms\Quantum-\docker

# Build and start (first time - takes 5-10 minutes)
docker-compose up --build

# Or run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

**What happens automatically:**
1. ✅ Builds Docker image with Python 3.12
2. ✅ Installs FFmpeg 8.0+
3. ✅ Installs Manim Community 0.20.1
4. ✅ Installs LaTeX (texlive) for mathematical rendering
5. ✅ Installs all pip dependencies from requirements.txt
6. ✅ Creates output directories
7. ✅ Initializes database
8. ✅ Starts Flask server on port 5000
9. ✅ Sets up health checks
10. ✅ Configures volume persistence

### Option B: Docker CLI (Advanced)

```bash
# Build image
docker build -t quantum-lms:latest -f docker/Dockerfile .

# Run container
docker run -d \
  --name quantum-lms \
  -p 5000:5000 \
  --env-file .env \
  -v "$(pwd)/quantum_lms.db:/app/quantum_lms.db" \
  -v "$(pwd)/output:/app/output" \
  -v "$(pwd)/media:/app/media" \
  quantum-lms:latest

# View logs
docker logs -f quantum-lms

# Stop
docker stop quantum-lms
docker rm quantum-lms
```

---

## 🏗️ Architecture

### Container Components

```
┌─────────────────────────────────────────┐
│  Quantum LMS Docker Container           │
├─────────────────────────────────────────┤
│  Base: python:3.12-slim-bookworm        │
│                                         │
│  System Packages:                       │
│   • FFmpeg 8.0                          │
│   • LaTeX (texlive)                     │
│   • Cairo & Pango                       │
│   • OpenCV dependencies                 │
│                                         │
│  Python Environment:                    │
│   • Flask 3.1.3                         │
│   • Manim CE 0.20.1                     │
│   • OpenCV, NumPy, scikit-learn         │
│   • LangChain-Groq                      │
│   • gTTS                                │
│   • All requirements.txt packages       │
│                                         │
│  Application:                           │
│   • Quantum LMS Flask app               │
│   • SQLite database                     │
│   • Video generator service             │
│   • AI chatbot service                  │
│                                         │
│  Exposed Port: 5000                     │
└─────────────────────────────────────────┘
         ↓
    127.0.0.1:5000
```

### Volume Mounts (Data Persistence)

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `quantum_lms.db` | `/app/quantum_lms.db` | SQLite database |
| `output/` | `/app/output` | Generated videos/audio |
| `media/` | `/app/media` | Manim render cache |

**Important**: Data persists even when container is stopped/removed

---

## 🔧 Configuration

### Environment Variables

The `.env` file is already configured in the project root (parent of docker/ folder) with the necessary credentials:

```env
# Required
GROQ_API_KEY=gsk_your_groq_api_key_here
SECRET_KEY=your_secret_key_min_64_chars

# Optional (defaults provided)
FLASK_APP=app.py
FLASK_ENV=production
```

Docker automatically loads these variables from the `.env` file.

### Resource Limits

Edit `docker-compose.yml` to adjust:

```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'      # Max 2 CPU cores
      memory: 4G       # Max 4GB RAM
    reservations:
      cpus: '1.0'      # Reserve 1 core
      memory: 2G       # Reserve 2GB
```

**Recommendations**:
- **Development**: 1 CPU, 2GB RAM
- **Production**: 2-4 CPUs, 4-8GB RAM (depending on concurrent video generation)

### Port Configuration

Change exposed port in `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Access at http://127.0.0.1:8080
```

---

## 🛠️ Management Commands

### Container Lifecycle

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View status
docker-compose ps

# View resource usage
docker stats quantum-lms-app
```

### Logs & Debugging

```bash
# View all logs
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# View last 50 lines
docker-compose logs --tail=50

# View specific service logs
docker logs quantum-lms-app

# Enter container shell
docker exec -it quantum-lms-app bash
```

### Database Access

```bash
# Backup database
docker exec quantum-lms-app sqlite3 /app/quantum_lms.db ".backup /app/output/backup.db"
docker cp quantum-lms-app:/app/output/backup.db ./backup-$(date +%Y%m%d).db

# Restore database
docker cp ./backup.db quantum-lms-app:/app/quantum_lms.db
docker-compose restart
```

### Updates & Rebuilds

```bash
# Rebuild after code changes
docker-compose up --build

# Force rebuild without cache
docker-compose build --no-cache
docker-compose up

# Pull latest base images
docker-compose build --pull
```

---

## 🐛 Troubleshooting

### Issue 1: "Port 5000 is already allocated"

**Solution 1**: Stop conflicting service
```bash
docker ps  # Find container using port 5000
docker stop <container-name>
```

**Solution 2**: Change port
```yaml
# In docker-compose.yml
ports:
  - "8080:5000"  # Use port 8080 instead
```

### Issue 2: "Cannot connect to Docker daemon"

**Windows**: Start Docker Desktop application

**Linux**:
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Issue 3: "GROQ_API_KEY not set" warning

```bash
# Check .env file exists
cat .env

# Should contain:
# GROQ_API_KEY=gsk_...

# Rebuild to load new env vars
docker-compose down
docker-compose up --build
```

### Issue 4: Video generation fails in container

```bash
# Enter container
docker exec -it quantum-lms-app bash

# Test Manim
python test_manim.py

# Check FFmpeg
ffmpeg -version

# View detailed logs
exit
docker-compose logs | grep "STEP 4/5"
```

### Issue 5: "No space left on device"

```bash
# Clean up Docker
docker system prune -a  # Remove unused images
docker volume prune     # Remove unused volumes

# Check disk usage
docker system df
```

### Issue 6: Build takes too long

**First time**: 5-10 minutes is normal (downloading base images, installing packages)

**Subsequent builds**: Should be faster due to Docker layer caching

**Speed up**:
```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1  # Linux/Mac
$env:DOCKER_BUILDKIT=1     # Windows PowerShell

docker-compose build
```

### Issue 7: Container keeps restarting

```bash
# Check logs for errors
docker-compose logs

# Common causes:
# - Missing .env file
# - Invalid GROQ_API_KEY
# - Database corruption
# - Port conflict

# Test health check manually
docker exec quantum-lms-app curl http://localhost:5000/health
```

---

## 🔒 Security Best Practices

### Production Deployment

1. **Change default credentials**
```bash
docker exec -it quantum-lms-app bash
# Inside container, update database users
```

2. **Use secrets management**
```bash
# Don't use .env file in production
# Use Docker secrets, AWS Secrets Manager, etc.
```

3. **Enable HTTPS** with reverse proxy (nginx/Traefik)

4. **Scan for vulnerabilities**
```bash
docker scan quantum-lms:latest
```

5. **Run as non-root** (already configured in Dockerfile)

6. **Limit resources** (already configured in docker-compose.yml)

### Network Security

```yaml
# In docker-compose.yml, add custom network
networks:
  quantum-lms-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

---

## 🌐 Production Deployment

### Cloud Platforms

#### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag quantum-lms:latest <account>.dkr.ecr.us-east-1.amazonaws.com/quantum-lms:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/quantum-lms:latest
```

#### Azure Container Instances
```bash
az acr build --registry <registry-name> --image quantum-lms:latest .
az container create --resource-group myResourceGroup --name quantum-lms --image <registry-name>.azurecr.io/quantum-lms:latest --dns-name-label quantum-lms --ports 5000
```

#### Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/<project-id>/quantum-lms
gcloud run deploy --image gcr.io/<project-id>/quantum-lms --platform managed
```

### Kubernetes

See `docker/k8s-deployment.yaml` for Kubernetes manifests (create if needed for K8s deployment).

---

## 📊 Monitoring

### Health Checks

**Automatic health check** runs every 30 seconds:
```bash
# Test health endpoint manually
curl http://127.0.0.1:5000/health
```

**Add health endpoint to Flask app** (if not exists):
```python
@app.route('/health')
def health():
    return {'status': 'healthy', 'service': 'quantum-lms'}
```

### Resource Monitoring

```bash
# Real-time stats
docker stats quantum-lms-app

# Container inspect
docker inspect quantum-lms-app

# Disk usage
docker system df
```

---

## 🔄 CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/docker-build.yml`:
```yaml
name: Docker Build and Push

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t quantum-lms:${{ github.sha }} -f docker/Dockerfile .
      - name: Run tests
        run: docker run quantum-lms:${{ github.sha }} python test_manim.py
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Manim Docker Guide](https://docs.manim.community/en/stable/installation/docker.html)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)

---

## 🆘 Getting Help

1. **Check logs**: `docker-compose logs -f`
2. **Enter container**: `docker exec -it quantum-lms-app bash`
3. **Verify installations**: `python test_manim.py`
4. **Review**: [MANIM_TROUBLESHOOTING.md](MANIM_TROUBLESHOOTING.md)
5. **Docker folder README**: [docker/README.md](docker/README.md)

---

**Updated**: 2026-02-28  
**Tested with**: Docker 24.0+, Docker Compose 2.20+, Windows 11/Ubuntu 22.04/macOS 13+
