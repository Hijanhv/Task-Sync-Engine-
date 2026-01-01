# 🚀 Quick Start Guide

Get your Task Sync Engine running in 5 minutes!

## Step 1: Prerequisites

Install Docker Desktop:
- **Windows**: https://docs.docker.com/desktop/install/windows-install/
- **Mac**: https://docs.docker.com/desktop/install/mac-install/
- **Linux**: https://docs.docker.com/engine/install/

## Step 2: Start the Application

Open terminal and run:

```bash
docker-compose up -d
```

That's it! The application is now running.

## Step 3: Access the Dashboard

Open your browser to:

**http://localhost:8000**

## Step 4: First Time Setup

### Option A: Setup Wizard (Recommended)

1. Go to http://localhost:8000/static/setup.html
2. Follow the 5-step visual setup
3. No coding required!

### Option B: Use Mock Data (Testing)

The app works out-of-the-box with mock data. Just:

1. Click "Sync Now" button
2. See sync results instantly
3. View sync history

## Common Commands

```bash
# View logs
docker-compose logs -f

# Stop application
docker-compose down

# Restart application
docker-compose restart

# Check status
docker-compose ps
```

## Configure Sync Mode

Edit `docker-compose.yml`:

**Manual Mode (default)**:
```yaml
AUTO_SYNC_ENABLED=false
```

**Automatic Mode**:
```yaml
AUTO_SYNC_ENABLED=true
SYNC_INTERVAL_SECONDS=300
```

Then restart:
```bash
docker-compose restart
```

## Troubleshooting

**Port 8000 in use?**
```bash
lsof -i :8000
# Or change port in docker-compose.yml to 8001:8000
```

**Docker not running?**
- Start Docker Desktop
- Verify: `docker ps`

**Can't access dashboard?**
- Try http://127.0.0.1:8000
- Check logs: `docker-compose logs`

## Next Steps

1. ✅ Complete setup wizard
2. ✅ Add your integrations (Jira, GitHub, etc.)
3. ✅ Create sync rules
4. ✅ Test with dry-run
5. ✅ Enable auto-sync

## Support

- Check DEPLOYMENT.md for detailed deployment options
- Review README.md for architecture details
- Check logs for errors: `docker-compose logs`

---

**You're all set!** Start syncing your tasks across platforms.
