# 🚀 Deployment Guide for Non-Technical Users

This guide will help you deploy Task Sync Engine **without writing any code**. Perfect for companies and teams who want to get started quickly!

---

## 📋 Table of Contents

1. [Quick Start (5 minutes)](#quick-start)
2. [Deployment Options](#deployment-options)
3. [Docker Deployment (Recommended)](#docker-deployment)
4. [Cloud Deployment (DigitalOcean)](#cloud-deployment)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Quick Start

### What You Need
- A computer (Windows, Mac, or Linux)
- Internet connection
- 10 minutes of your time

**No coding skills required!**

---

## 🐳 Docker Deployment (Recommended)

Docker makes deployment super simple - just one command!

### Step 1: Install Docker

#### On Windows
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Run the installer
3. Follow the setup wizard
4. Restart your computer

#### On Mac
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Open the .dmg file
3. Drag Docker to Applications
4. Launch Docker from Applications

#### On Linux (Ubuntu/Debian)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Step 2: Download Task Sync Engine

**Option A: Download ZIP**
1. Go to the GitHub repository
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to a folder

**Option B: Use Git (if you have it)**
```bash
git clone https://github.com/your-username/task-sync-engine.git
cd task-sync-engine
```

### Step 3: Start the Application

Open your terminal/command prompt in the project folder and run:

```bash
docker-compose up -d
```

That's it! The application is now running.

### Step 4: Access the Application

Open your web browser and go to:
```
http://localhost:8000
```

You should see the setup wizard! 🎉

### Step 5: Complete Setup Wizard

1. Click through the welcome screen
2. Select the integrations you want (Jira, GitHub, Trello, etc.)
3. Enter your credentials for each platform
4. Configure sync settings
5. Done!

---

## ☁️ Cloud Deployment (DigitalOcean)

Deploy to the cloud in 10 minutes - no command line needed!

### Step 1: Create DigitalOcean Account

1. Go to [DigitalOcean.com](https://www.digitalocean.com)
2. Sign up (get $200 free credit!)
3. Verify your email

### Step 2: Create a Droplet

1. Click "Create" → "Droplets"
2. Choose image: **Docker** (under Marketplace)
3. Choose plan: **$6/month** (sufficient for most cases)
4. Choose datacenter: **Select closest to you**
5. Authentication: **Create SSH key** or use password
6. Click **Create Droplet**

### Step 3: Access Your Server

#### Using Web Console (Easiest)
1. Click on your droplet name
2. Click "Access" → "Launch Droplet Console"
3. Log in with your credentials

#### Using SSH (Mac/Linux)
```bash
ssh root@your_droplet_ip
```

### Step 4: Deploy the Application

Copy and paste these commands one by one:

```bash
# Download the application
git clone https://github.com/your-username/task-sync-engine.git
cd task-sync-engine

# Start the application
docker-compose up -d

# Check if it's running
docker ps
```

### Step 5: Configure Firewall

```bash
# Allow HTTP traffic
ufw allow 8000/tcp
```

### Step 6: Access Your Application

Open your browser and go to:
```
http://your_droplet_ip:8000
```

Replace `your_droplet_ip` with the IP address shown in DigitalOcean.

### Optional: Set Up Domain Name

1. Buy a domain (e.g., from Namecheap, GoDaddy)
2. In your domain settings, add an **A Record**:
   - Type: `A`
   - Host: `@`
   - Value: `your_droplet_ip`
3. Wait 5-10 minutes for DNS propagation
4. Access via: `http://yourdomain.com:8000`

---

## 🎮 Configuration (No Coding!)

### Method 1: Using the Web Interface (Easiest)

1. Go to `http://localhost:8000/static/setup.html`
2. Follow the setup wizard
3. All configuration is done through clicks and forms!

### Method 2: Settings Page

1. Go to your dashboard
2. Click "⚙️ Settings" button
3. Configure:
   - **Auto-sync**: Enable/disable automatic sync
   - **Sync Interval**: How often to sync
   - **Email Notifications**: Get alerts
   - **Timezone**: Your local timezone

### Method 3: Environment Variables (Advanced)

If you want to set defaults before starting, edit `docker-compose.yml`:

```yaml
environment:
  - AUTO_SYNC_ENABLED=true      # Enable bot mode
  - SYNC_INTERVAL_SECONDS=300   # Sync every 5 minutes
```

Then restart:
```bash
docker-compose restart
```

---

## 🔌 Adding Integrations

### No Coding Required!

1. Go to Settings page
2. Click "➕ Add New Integration"
3. Choose your platform (Jira, GitHub, Trello, etc.)
4. Fill in the form with your credentials
5. Click "🔍 Test" to verify connection
6. Click "Save Integration"

### Getting API Credentials

#### Jira
1. Go to [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Copy the token
4. Use your email and token in the setup

#### GitHub
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select scopes: `repo`, `read:org`
4. Copy the token

#### Trello
1. Go to [trello.com/app-key](https://trello.com/app-key)
2. Copy your API Key
3. Click the token link and authorize
4. Copy the token

---

## 🔄 Managing Syncs

### Manual Sync (User Tool Mode)
1. Go to your dashboard
2. Click "🔄 Sync Now" button
3. View results immediately

### Automatic Sync (Bot Mode)
1. Go to Settings
2. Enable "Automatic Sync"
3. Choose interval (e.g., every 5 minutes)
4. Save settings
5. Sync runs automatically in background!

---

## 📊 Monitoring

### View Sync History
1. Dashboard shows recent syncs
2. See what was synced, when, and any errors
3. Click "Refresh Status" for latest info

### Check Health
- Green badge = Everything working
- Red badge = Issues detected
- Click for details

---

## 🛑 Stopping the Application

```bash
# Stop the application
docker-compose down

# Stop and remove all data
docker-compose down -v
```

---

## 🔧 Troubleshooting

### Application Won't Start

**Problem**: Error when running docker-compose
```bash
# Check Docker is running
docker --version

# View logs
docker-compose logs
```

**Solution**: Make sure Docker Desktop is running

### Can't Access Web Interface

**Problem**: Browser shows "Can't connect"

**Check**:
1. Is Docker running? Check Docker Desktop
2. Is the container running? Run: `docker ps`
3. Try: `http://localhost:8000` or `http://127.0.0.1:8000`

### Sync Not Working

**Problem**: Sync fails or doesn't run

**Check**:
1. Are integrations configured? Go to Settings
2. Are credentials correct? Test connection
3. Is auto-sync enabled? Check Settings
4. View logs: `docker-compose logs -f`

### Port Already in Use

**Problem**: Port 8000 is already in use

**Solution**: Edit `docker-compose.yml` and change:
```yaml
ports:
  - "8080:8000"  # Use port 8080 instead
```

Then access via: `http://localhost:8080`

---

## 🔐 Security Best Practices

### For Production Use

1. **Change Default Settings**
   - Use strong passwords
   - Don't share API keys

2. **Use HTTPS**
   - Set up SSL certificate (free with Let's Encrypt)
   - Use a reverse proxy (Nginx)

3. **Regular Backups**
   ```bash
   # Backup configuration
   docker cp task-sync-engine:/app/user_config.json ./backup.json
   ```

4. **Keep Updated**
   ```bash
   # Update to latest version
   docker-compose pull
   docker-compose up -d
   ```

---

## 🆘 Getting Help

### Community Support
- 📖 Check the [documentation](../docs/)
- 💬 Join our Discord/Slack community
- 🐛 Report issues on GitHub

### Professional Support
- 📧 Email: support@tasksync.com
- 💼 Enterprise plans available

---

## ✅ Checklist

Before going to production:

- [ ] Docker installed and running
- [ ] Application accessible via browser
- [ ] Setup wizard completed
- [ ] Integrations tested and working
- [ ] Auto-sync configured (if needed)
- [ ] Email notifications set up
- [ ] Backup created
- [ ] Security settings reviewed
- [ ] Team members trained

---

## 🎓 Video Tutorials

Coming soon:
- 📹 Complete setup walkthrough
- 📹 Adding your first integration
- 📹 Troubleshooting common issues
- 📹 Advanced configuration

---

## 💡 Tips for Success

1. **Start Small**: Connect just 2 platforms first
2. **Test Often**: Use manual sync to test before enabling auto-sync
3. **Monitor Daily**: Check sync history regularly in the first week
4. **Document**: Keep a note of your API keys and settings
5. **Backup**: Export your configuration weekly

---

## 🎉 You're Ready!

You've successfully deployed Task Sync Engine without writing a single line of code!

**Next Steps:**
1. Complete the setup wizard
2. Add your first integration
3. Run your first sync
4. Enable auto-sync once comfortable

**Questions?** We're here to help! Check the [FAQ](../docs/faq.md) or reach out to support.

---

**Built for non-technical users | Zero coding required | Production-ready**
