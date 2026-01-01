# 🚀 Deployment Guide

This guide explains how to deploy the Task Sync Engine in different environments.

## 📋 Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- 2GB free disk space
- Port 8000 available

## 🏃 Quick Start (Docker Compose)

### 1. Clone and Navigate

```bash
cd task-sync-engine
```

### 2. Configure Environment (Optional)

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Edit `.env` to set:
- `AUTO_SYNC_ENABLED=true` (for automatic mode)
- `SYNC_INTERVAL_SECONDS=300` (sync every 5 minutes)

### 3. Start the Application

```bash
docker-compose up -d
```

### 4. Access the Dashboard

Open your browser to: **http://localhost:8000**

### 5. Complete Setup

Follow the setup wizard at: **http://localhost:8000/static/setup.html**

## 🛑 Stop the Application

```bash
docker-compose down
```

## 🔄 Update the Application

```bash
docker-compose down
docker-compose pull
docker-compose up -d
```

## 📊 View Logs

```bash
# View all logs
docker-compose logs -f

# View last 50 lines
docker-compose logs --tail=50 -f
```

## 🐳 Docker Commands Reference

```bash
# Start in foreground (see logs)
docker-compose up

# Start in background
docker-compose up -d

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# View container status
docker-compose ps

# Rebuild after code changes
docker-compose build
docker-compose up -d
```

## 🌐 Production Deployment

### Using Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Create new project from GitHub repo
4. Railway auto-detects Dockerfile
5. Set environment variables in Railway dashboard
6. Deploy!

### Using Vercel (Frontend) + Railway (Backend)

**Backend on Railway:**
1. Deploy backend as described above
2. Note the Railway URL (e.g., `https://your-app.railway.app`)

**Frontend on Vercel:**
1. Update `frontend/script.js` to use Railway URL
2. Push to GitHub
3. Import project to Vercel
4. Deploy

### Using AWS ECS/Fargate

1. Build and push image to ECR
2. Create ECS task definition using Dockerfile
3. Create ECS service
4. Configure load balancer on port 8000
5. Set environment variables in task definition

### Using DigitalOcean App Platform

1. Connect GitHub repository
2. Select Dockerfile build method
3. Set environment variables
4. Deploy

## 🔒 Security Considerations for Production

### 1. Environment Variables

Never commit `.env` files. Use platform-specific secret management:

- **Railway**: Environment Variables dashboard
- **Vercel**: Environment Variables settings
- **AWS**: AWS Secrets Manager
- **Docker**: Docker secrets

### 2. HTTPS/SSL

Enable HTTPS for production deployments:

- Railway: Automatic HTTPS
- Vercel: Automatic HTTPS
- Custom domain: Use Let's Encrypt or CloudFlare

### 3. API Keys

Store integration credentials securely:

```python
# Use environment variables
JIRA_API_KEY = os.getenv("JIRA_API_KEY")

# Or platform secret management
# Railway: Encrypted environment variables
# AWS: Secrets Manager
```

### 4. CORS Configuration

Update `backend/app/config.py` for production:

```python
CORS_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```

## ⚙️ Configuration Options

### Mode Selection

**User Tool Mode** (Manual only):
```yaml
environment:
  - AUTO_SYNC_ENABLED=false
```

**Bot Mode** (Automatic + Manual):
```yaml
environment:
  - AUTO_SYNC_ENABLED=true
  - SYNC_INTERVAL_SECONDS=300
```

### Database Configuration (Future)

When using PostgreSQL:

```yaml
environment:
  - DATABASE_URL=postgresql://user:password@db:5432/tasksync
```

Uncomment PostgreSQL service in `docker-compose.yml`.

## 🔍 Troubleshooting

### Port 8000 Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill the process or change port in docker-compose.yml
ports:
  - "8001:8000"
```

### Container Won't Start

```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Can't Access Dashboard

1. Verify container is running: `docker-compose ps`
2. Check logs: `docker-compose logs`
3. Verify port mapping: `docker-compose ps`
4. Try `http://127.0.0.1:8000` instead

### Auto-Sync Not Working

1. Check environment variable: `AUTO_SYNC_ENABLED=true`
2. Restart container: `docker-compose restart`
3. View logs for scheduler messages: `docker-compose logs -f`

## 📦 Data Persistence

User configurations are stored in `./data` directory:

```yaml
volumes:
  - ./data:/app/data
```

**Backup your data:**

```bash
# Backup
cp -r ./data ./data-backup-$(date +%Y%m%d)

# Restore
cp -r ./data-backup-20260101 ./data
```

## 🚀 Performance Optimization

### 1. Use PostgreSQL for Production

Uncomment PostgreSQL in `docker-compose.yml`:

```yaml
postgres:
  image: postgres:15-alpine
  # ... configuration
```

### 2. Add Redis Cache

Uncomment Redis in `docker-compose.yml`:

```yaml
redis:
  image: redis:7-alpine
  # ... configuration
```

### 3. Adjust Sync Interval

```yaml
environment:
  - SYNC_INTERVAL_SECONDS=600  # 10 minutes instead of 5
```

## 📱 Mobile Access

Access from mobile devices on the same network:

1. Find your computer's IP: `ifconfig` (Mac/Linux) or `ipconfig` (Windows)
2. Open `http://YOUR_IP:8000` on mobile browser

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## ✅ Health Check

Verify deployment is working:

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "app_name": "Task Sync Engine",
  "version": "1.0.0",
  "mode": "user-tool",
  "auto_sync_enabled": false
}
```

## 📞 Support

If you encounter issues:

1. Check this guide first
2. Review logs: `docker-compose logs`
3. Check GitHub Issues
4. Verify Docker is running: `docker ps`

## 🎯 Next Steps

After deployment:

1. Complete the setup wizard
2. Add your first integration
3. Create a sync rule
4. Test with dry-run
5. Enable auto-sync if needed

---

**Deployment complete!** Your Task Sync Engine is now running and ready to use.
