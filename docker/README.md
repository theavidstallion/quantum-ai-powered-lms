# Docker Setup for Quantum LMS

This folder contains all Docker configuration files for running Quantum LMS in a containerized environment.

## 📁 Files in this Folder

- **Dockerfile** - Multi-stage build with Python 3.12, FFmpeg, Manim CE, LaTeX
- **docker-compose.yml** - Orchestration config with health checks and resource limits
- **entrypoint.sh** - Startup script with dependency verification
- **.dockerignore** - Excludes unnecessary files from Docker context
- **README.md** - This file

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed ([download here](https://www.docker.com/products/docker-desktop))
- `.env` file with credentials already configured in parent directory

### Option 1: Using Docker Compose (Recommended)
```bash
# From project root (Quantum-/)
cd docker
docker-compose up --build

# Access app at: http://127.0.0.1:5000
# Login: admin / admin123

# All dependencies install automatically:
# ✅ Python 3.12, FFmpeg, Manim CE, LaTeX, all pip packages
```

### Option 2: Using Docker CLI
```bash
# Build image
cd docker
docker build -t quantum-lms:latest -f Dockerfile ..

# Run container
docker run -d \
  --name quantum-lms \
  -p 5000:5000 \
  --env-file ../.env \
  -v "$(pwd)/../quantum_lms.db:/app/quantum_lms.db" \
  -v "$(pwd)/../output:/app/output" \
  quantum-lms:latest

# Access app at: http://127.0.0.1:5000
```

## 🔧 What Gets Installed Automatically

### System Dependencies
- ✅ **FFmpeg 8.0+** - Video processing
- ✅ **LaTeX (texlive)** - Mathematical equations
- ✅ **Cairo & Pango** - Manim rendering backend
- ✅ **OpenCV dependencies** - Computer vision libraries

### Python Packages (from requirements.txt)
- ✅ **Flask 3.1.3** - Web framework
- ✅ **Manim Community 0.20.1** - Animation engine
- ✅ **OpenCV, NumPy, scikit-learn** - Data processing
- ✅ **LangChain, Groq** - AI chatbot
- ✅ **gTTS** - Text-to-speech
- ✅ All other dependencies from requirements.txt

## 📊 Container Details

### Ports
- **5000** - Flask web server

### Volumes (Data Persistence)
- `quantum_lms.db` - SQLite database
- `output/` - Generated videos and audio files
- `media/` - Manim render cache

### Resource Limits
- **CPU**: 2 cores max, 1 core reserved
- **Memory**: 4GB max, 2GB reserved
- Adjust in `docker-compose.yml` if needed

### Health Check
- Runs every 30 seconds
- Checks if Flask server responds at `/health`
- 3 retries before marking unhealthy

## 🛠️ Common Commands

### Start Services
```bash
cd docker
docker-compose up -d  # Detached mode (background)
```

### View Logs
```bash
docker-compose logs -f  # Follow logs
docker logs quantum-lms-app  # Direct container logs
```

### Stop Services
```bash
docker-compose down  # Stop and remove containers
docker-compose down -v  # Also remove volumes (CAREFUL: deletes data)
```

### Restart
```bash
docker-compose restart
```

### Rebuild After Code Changes
```bash
docker-compose up --build  # Rebuild and start
```

### Enter Container Shell
```bash
docker exec -it quantum-lms-app bash
# Now you're inside the container
python test_manim.py  # Test Manim
exit
```

### Check Container Status
```bash
docker ps  # Running containers
docker-compose ps  # Services status
docker stats quantum-lms-app  # Resource usage
```

## 🐛 Troubleshooting

### Issue: Port 5000 already in use
```bash
# Stop conflicting service
docker ps  # Find container using port 5000
docker stop <container-id>

# Or change port in docker-compose.yml:
ports:
  - "8080:5000"  # Access at http://127.0.0.1:8080
```

### Issue: "GROQ_API_KEY not set" warning
```bash
# Ensure .env file exists in parent directory
cd ..
cat .env  # Should contain GROQ_API_KEY=gsk_...

# Rebuild container
cd docker
docker-compose down
docker-compose up --build
```

### Issue: "Database locked" errors
```bash
# Stop all containers accessing the database
docker-compose down

# Remove database lock
cd ..
rm quantum_lms.db-journal  # If exists

# Restart
cd docker
docker-compose up
```

### Issue: Video generation fails
```bash
# Check FFmpeg inside container
docker exec -it quantum-lms-app bash
ffmpeg -version
python -c "import manim; print(manim.__version__)"
exit

# Check logs for detailed error
docker-compose logs | grep "STEP 4/5"
```

### Issue: Out of disk space
```bash
# Clean up unused Docker resources
docker system prune -a  # Remove all unused images
docker volume prune  # Remove unused volumes

# Check disk usage
docker system df
```

### Issue: Slow build times
```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker-compose build

# Or enable globally (Linux/Mac)
export DOCKER_BUILDKIT=1
```

## 🔒 Security Notes

### Production Deployment
1. **Change default passwords** in database
2. **Use production-grade SECRET_KEY** (64+ chars)
3. **Enable HTTPS** with reverse proxy (nginx/traefik)
4. **Set environment to production**:
   ```yaml
   environment:
     - FLASK_ENV=production
   ```
5. **Scan for vulnerabilities**:
   ```bash
   docker scan quantum-lms:latest
   ```

### Environment Variables
Never commit `.env` file to Git. Use secrets management in production:
- Docker Swarm: `docker secret`
- Kubernetes: `kubectl create secret`
- Cloud: AWS Secrets Manager, Azure Key Vault, etc.

## 📈 Performance Tips

### Development Mode
Uncomment this line in `docker-compose.yml` to sync code changes without rebuilding:
```yaml
volumes:
  - ..:/app  # Live code reload
```
*Note: Restart container after code changes (Flask use_reloader=False)*

### Production Mode
- Use pre-built images (push to Docker Hub)
- Enable horizontal scaling with Docker Swarm or Kubernetes
- Add Redis for session storage (currently in-memory)
- Use external PostgreSQL instead of SQLite for multi-container deployments

### Resource Optimization
For low-resource environments, reduce limits in `docker-compose.yml`:
```yaml
resources:
  limits:
    cpus: '1.0'
    memory: 2G
```

## 🌐 Networking

### Access from Other Devices
By default, Flask binds to `127.0.0.1` (localhost only). To access from other devices:

1. Modify [app.py](../app.py#L366):
   ```python
   app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
   ```
2. Rebuild container:
   ```bash
   docker-compose up --build
   ```
3. Access from other devices on same network:
   ```
   http://<your-ip>:5000
   ```

### Reverse Proxy Setup (nginx)
```nginx
server {
    listen 80;
    server_name quantum-lms.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📦 Image Size
Expected Docker image size: **~2.5-3GB** (includes LaTeX, FFmpeg, Python libs)

To reduce size:
- Remove LaTeX if not using complex math (saves ~800MB)
- Use `python:3.12-slim` base (already optimized)
- Multi-stage builds (already implemented)

## 🔄 Update Guide

### Update Dependencies
```bash
# Update requirements.txt in parent directory
cd ..
pip freeze > requirements.txt

# Rebuild Docker image
cd docker
docker-compose build --no-cache
docker-compose up -d
```

### Update Base Image
```bash
# Pull latest Python 3.12
docker pull python:3.12-slim-bookworm

# Rebuild
docker-compose build --pull
```

## 🧪 Testing

### Test Container Build
```bash
cd docker
docker build -t quantum-lms:test -f Dockerfile ..
docker run --rm quantum-lms:test python test_manim.py
```

### Run Health Check Manually
```bash
docker exec quantum-lms-app python -c "import requests; print(requests.get('http://localhost:5000/health', timeout=5).json())"
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Manim Docker Setup](https://docs.manim.community/en/stable/installation/docker.html)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)

## 🆘 Support

If you encounter issues:
1. Check logs: `docker-compose logs -f`
2. Verify `.env` file exists with correct keys
3. Ensure Docker Desktop is running
4. Check disk space: `docker system df`
5. Review [MANIM_TROUBLESHOOTING.md](../MANIM_TROUBLESHOOTING.md)

---

**Last Updated**: 2026-02-28  
**Docker Version**: Tested with Docker 24.0+, Docker Compose 2.20+
