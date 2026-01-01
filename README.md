# 🔄 Task Sync Engine

A **zero-code task synchronization platform** that works as both a **user-triggered tool** and an **autonomous bot**. Perfect for non-technical users and companies!

## 🎯 No Coding Required!

**Everything is point-and-click:**
- ✅ Visual setup wizard
- ✅ Web-based configuration
- ✅ One-command deployment
- ✅ No technical skills needed

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Docker
Download [Docker Desktop](https://www.docker.com/products/docker-desktop/) for Windows or Mac

### Step 2: Start the Application
```bash
docker-compose up -d
```

### Step 3: Open Your Browser
Go to: **http://localhost:8000**

### Step 4: Complete Setup Wizard
Follow the visual wizard - no coding needed!

**📖 [Read Full Quick Start Guide →](docs/QUICKSTART.md)**

---

## 📁 Project Structure

```
task-sync-engine/
│
├── 🐳 docker-compose.yml        # One-command deployment
├── 🐳 Dockerfile               # Container configuration
│
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI entry point
│   │   ├── config.py           # Settings management
│   │   │
│   │   ├── routes/
│   │   │   ├── sync.py         # Sync endpoints (USER TOOL)
│   │   │   ├── health.py       # Health check
│   │   │   └── config.py       # No-code configuration API
│   │   │
│   │   ├── services/
│   │   │   ├── sync_engine.py  # Core sync logic (DUAL MODE)
│   │   │   ├── data_loader.py  # Integration connectors
│   │   │   └── logger.py       # Logging
│   │   │
│   │   ├── models/
│   │   │   └── task.py         # Task schema
│   │   │
│   │   └── db/
│   │       └── memory_db.py    # Storage
│   │
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── index.html              # Main dashboard
│   ├── setup.html              # 🎨 Setup wizard (NO CODE!)
│   ├── settings.html           # 🎨 Visual settings (NO CODE!)
│   ├── style.css               # Styling
│   └── script.js               # Frontend logic
│
├── docs/
│   ├── QUICKSTART.md           # 5-minute setup guide
│   ├── DEPLOYMENT.md           # Non-technical deployment
│   ├── architecture.md         # System architecture
│   ├── api.md                  # API documentation
│   └── roadmap.md             # Development roadmap
│
└── README.md                   # You are here!
```

---

## 🎯 Features

### ✅ No-Code Configuration
- **Setup Wizard** - 5-step visual setup
- **Web Interface** - Configure everything in your browser
- **Test Connections** - Verify integrations with one click
- **Visual Field Mapping** - Drag-and-drop field configuration (coming soon)

### ✅ Platform Integrations
Connect to popular platforms without API knowledge:
- 🎯 **Jira** - Project management
- 🐙 **GitHub Issues** - Issue tracking
- 📋 **Trello** - Kanban boards
- ✅ **Asana** - Tas (No Coding!)

### Option 1: Setup Wizard (Recommended)
1. Open http://localhost:8000/static/setup.html
2. Follow 5 visual steps
3. Done!

### Option 2: Settings Page
1. Go to dashboard
2. Click "⚙️ Settings"
3. Configure via forms

### Option 3: Docker Environment (Advanced)
Edit `docker-compose.yml`:
```yaml
environment:
  - AUTO_SYNC_ENABLED=true      # Enable bot mode
  - SYNC_INTERVAL_SECONDS=300   # Sync every 5 minutes
```

**📖 [Read Full Configuration Guide →](docs/DEPLOYMENT.md#configuration)**e          # Enable bot mode (True/False)
SYNC_INTERVAL_SECONDS=300        # Sync every 5 minutes

# External Systems (coming soon)
SOURCE_API_URL=https://...
DESTINATION_API_URL=https://...
```

### Modes

**User Tool Mode (Default):**
```env
AUTO_SYNC_ENABLED=False
```
- Manual sync only via UI/API
- Best for testing and demos

**Bot Mode (Autonomous):**
```env
AUTO_SYNC_ENABLED=True
SYNC_INTERVAL_SECONDS=300
```
- Automatic sync every 5 minutes
- Best for production

**Hy�️ Adding Integrations (No Code!)

### Via Setup Wizard
1. Open setup wizard
2. Select platforms (Jira, GitHub, etc.)
3. Enter credentials in web form
4. Test connection with one click
5. Save!

### Via Settings Page
1. Go to Settings
2. Click "➕ Add New Integration"
3. Choose platform
4. Fill in form fields
5. Test & Save

### Getting API Credentials

**Jira:**
1. Go to [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Copy and paste into form

**GitHub:**
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Copy and paste into form

**Trello:**
1. Go to [trello.com/app-key](https://trello.com/app-key)
2. Copy API key and token
3. Paste into form

**No API knowledge needed - just copy/paste!**
GET /api/sync/history?limit=10
```

### Dry Run
```bash
POST /api/sync/dry-run
```

**Full API documentation:** See [docs/api.md](docs/api.md)

---

## 🎨 Dashboard

Access the web dashboard at `http://localhost:8000`

Features:
- ⚡ **Sync Now** - Trigger manual sync (User Tool Mode)
- 🔍 **Dry Run** - Preview changes without applying
- 📊 **Status** - View current sync statistics
- 📜 **History** - See past sync operations
- ℹ️ **at `http://localhost:8000`

### Key Pages

**Main Dashboard** - `/`
- ⚡ Sync Now button (User Tool Mode)
- 📊 Real-time statistics
- 📜 Sync history
- ℹ️ System information

**Setup Wizard** - `/static/setup.html`
- 💡 For Non-Technical Users

### What You Can Do Without Coding

✅ **Connect your tools** - Just enter credentials in web forms
✅ **Set up sync** - Click and select options
✅ **Choose when to sync** - Toggle automatic/manual mode
✅ **Test connections** - One-click verification
✅ **Monitor syncs** - View dashboard
✅ **Manage settings** - All via web interface
✅ **Deploy anywhere** - One Docker command

### What You DON'T Need

❌ Programming knowledge
❌ Terminal/command line skills (optional)
❌ API understanding
❌ Database setup
❌ Server management
❌ Code editing

### Perfect For

- 👔 **Business teams** - No IT department needed
- 🏢 **Small companies** - Deploy in minutes
- 🎯 **Project managers** - Self-service setup
- 📊 **Product teams** - Connect tools easily
- 🚀 **Startups** - Quick integration solution
**📖 [Read Full Deployment Guide →](docs/DEPLOYMENT.md)**
import requests

# Trigger manual sync
response = requests.post('http://localhost:8000/api/sync')
result = response.json()
print(f"Sync completed: {result['success']}")
print(f"Added: {result['stats']['added']}")
print(f"Updated: {result['stats']['updated']}")
```

### cURL
```bash
# Health check
curl http://localhost:8000/api/health

# Trigger sync
curl -X POST http://localhost:8000/api/sync

# Get sync status
curl http://localhost:8000/api/sync/status
```

### JavaScript
```javascript
// Trigger sync from your app
fetch('http://localhost:8000/api/sync', {
  method: 'POST'
})
  .then(response => response.json())
  .then(data => console.log('Sync result:', data));
```

---

## 🏗️ Architecture

### Execution Flow

**User Tool Mode:**
```
User → Click Button → API Request → Sync Engine → External APIs → Result
```

**Bot Mode:**
```
Scheduler → Timer → Sync Engine → External APIs → Log Result → Repeat
```

### Key Components

1. **Sync Engine** - Core synchronization logic (used by both modes)
2. **Data Loader** - Interface with external systems
3. **API Routes** - HTTP endpoints for manual triggers
4. **Background Task** - Scheduler for automatic execution
5. **Memory DB** - Temporary storage (will be replaced with PostgreSQL)

**Full architecture:** See [docs/architecture.md](docs/architecture.md)

---

## 🧭 Roadmap

### Phase 1: Foundation ✅ COMPLETE
- [x] Project structure
- [x] FastAPI backend
- [x] Frontend dashboard
- [x] Dual execution modes
- [x] Documentation

### Phase 2: Real Integrations (Weeks 3-6)
- [ ] Jira integration
- [ ] GitHub Issues
- [ ] Trello
- [ ] Asana

### Phase 3: Database & Persistence (Weeks 7-8)
- [ ] PostgreSQL setup
- [ ] Redis caching
- [ ] Data migrations

### Phase 4: Advanced Features (Weeks 9-12)
- [ ] Conflict resolution
- [ ] Bi-directional sync
- [ ] Selective sync
- [ ] Transformation rules

**Full roadmap:** See [docs/roadmap.md](docs/roadmap.md)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💡 Interview-Ready Explanation

> "I built a task synchronization engine with **dual execution modes**. It supports both **manual triggers** via UI (acting as a user tool) and **automated execution** through scheduled tasks (acting as a bot). This allows it to function flexibly depending on the use case - humans can trigger syncs when needed, and the system can also run autonomously in the background. The same core sync logic is used in both cases, making it efficient and maintainable."

---

## 🎓 Key Learnings

This project demonstrates:

- **Dual-mode architecture** - Supporting both user-triggered and autonomous execution
- **FastAPI** - Modern Python web framework with async support
- **RESTful API design** - Clean, documented endpoints
- **Separation of concerns** - Clear service/route/model layers
- **Extensibility** - Easy to add new integrations
- **Real-world patterns** - Scheduling, background tasks, data sync

---

## 📞 Support

For questions or issues:
- 📖 Check the [documentation](docs/)
- 🐛 Open an [issue](https://github.com/your-username/task-sync-engine/issues)
- 💬 Join our community chat

---

**Built with ❤️ | Designed for both human control and autonomous operation**
A deployed Task Sync Engine that non-technical users and companies can use easily-without coding.
