# 🎯 Quick Start Guide

Get Task Sync Engine running in **5 minutes** - no coding required!

---

## ⚡ Fastest Way to Start

### 1️⃣ Install Docker

**Windows/Mac**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)

**Linux**:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2️⃣ Download & Start

```bash
# Download the project
git clone https://github.com/your-username/task-sync-engine.git
cd task-sync-engine

# Start the application (one command!)
docker-compose up -d
```

### 3️⃣ Open Your Browser

Go to: **http://localhost:8000**

### 4️⃣ Complete Setup Wizard

Follow the 5-step wizard:
1. ✅ Welcome
2. 🔌 Choose integrations (Jira, GitHub, etc.)
3. 🔑 Enter credentials
4. ⚙️ Configure settings
5. 🎉 Done!

---

## 🖱️ No Command Line? No Problem!

### Use Our One-Click Installers (Coming Soon)

- 🪟 **Windows Installer** - Double-click to install
- 🍎 **Mac App** - Drag to Applications
- ☁️ **Cloud Deploy Button** - Deploy to DigitalOcean in 1 click

---

## 🎨 What You Can Do (All No-Code)

### ✅ Connect Platforms
- Jira
- GitHub Issues
- Trello  
- Asana
- Linear
- ClickUp

All through web forms - **no API knowledge needed**!

### ✅ Set Up Sync Rules
- Choose what syncs where
- Set filters visually
- Map fields with dropdowns
- Test connections instantly

### ✅ Choose Your Mode

**User Tool Mode** (Manual)
- Click "Sync Now" when you want
- Perfect for testing

**Bot Mode** (Automatic)
- Syncs every 5 minutes (or your choice)
- Runs in background
- Perfect for production

### ✅ Monitor & Control
- Real-time dashboard
- Sync history
- Error notifications
- One-click sync testing

---

## 📱 Accessing Your Application

### Local Development
```
http://localhost:8000
```

### Cloud Deployment
```
http://your-server-ip:8000
```

### With Domain
```
http://yourdomain.com:8000
```

---

## 🔧 Basic Management

### View Status
```bash
docker-compose ps
```

### View Logs
```bash
docker-compose logs -f
```

### Stop Application
```bash
docker-compose down
```

### Restart Application
```bash
docker-compose restart
```

### Update to Latest Version
```bash
docker-compose pull
docker-compose up -d
```

---

## 🆘 Having Issues?

### Can't Access http://localhost:8000?

**Try these**:
1. Check Docker is running (Docker Desktop icon)
2. Run: `docker ps` to verify container is running
3. Try: `http://127.0.0.1:8000`

### Port Already in Use?

Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Change to 8080 or any free port
```

Then restart: `docker-compose restart`

### Integration Not Working?

1. Go to Settings page
2. Click "🔍 Test" button on your integration
3. Check credentials are correct
4. Verify API permissions

---

## 📚 Next Steps

1. ✅ [Complete Setup Wizard](http://localhost:8000/static/setup.html)
2. ⚙️ [Configure Settings](http://localhost:8000/static/settings.html)
3. 📊 [View Dashboard](http://localhost:8000)
4. 📖 [Read Full Documentation](./DEPLOYMENT.md)

---

## 💡 Pro Tips

🎯 **Start with 2 platforms** - Don't overwhelm yourself

🧪 **Test first** - Use manual sync before enabling auto-sync

📅 **Check daily** - Monitor sync history in the first week

💾 **Backup settings** - Export your configuration

🔔 **Set up notifications** - Get email alerts for errors

---

## 🎓 Video Walkthrough (Coming Soon)

- 📹 5-minute setup from scratch
- 📹 Adding your first Jira integration
- 📹 Setting up automatic sync
- 📹 Troubleshooting common issues

---

## ✨ Features at a Glance

| Feature | Status | Code Required? |
|---------|--------|----------------|
| Connect Jira | ✅ | ❌ No |
| Connect GitHub | ✅ | ❌ No |
| Connect Trello | ✅ | ❌ No |
| Manual Sync | ✅ | ❌ No |
| Auto Sync | ✅ | ❌ No |
| Test Connections | ✅ | ❌ No |
| Visual Setup | ✅ | ❌ No |
| Sync History | ✅ | ❌ No |
| Email Alerts | ✅ | ❌ No |

**Everything is point-and-click!** 🖱️

---

## 🤝 Need Help?

- 📖 [Full Deployment Guide](./DEPLOYMENT.md)
- 🏗️ [Architecture Documentation](./architecture.md)
- 🔌 [API Reference](./api.md)
- 🗺️ [Roadmap](./roadmap.md)
- 💬 Community Discord (link here)
- 📧 Email Support: support@tasksync.com

---

**🎉 Congratulations!** You're running a production-ready task sync engine without writing a single line of code!
