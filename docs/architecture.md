# Architecture Documentation

## Overview

The Task Sync Engine is a **dual-mode synchronization system** that operates both as:
1. **User-Triggered Tool** - Manual execution via UI/API
2. **Autonomous Bot** - Automatic execution via scheduler

This architecture allows maximum flexibility for different use cases while maintaining a single, consistent sync logic.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (UI)                        │
│  - Dashboard for manual sync triggering                  │
│  - Real-time status display                              │
│  - Sync history visualization                            │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ HTTP/REST
                 │
┌────────────────▼────────────────────────────────────────┐
│                   FastAPI Backend                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │            Routes/Endpoints                       │  │
│  │  - /api/sync (POST) - Manual trigger             │  │
│  │  - /api/sync/status (GET)                        │  │
│  │  - /api/sync/history (GET)                       │  │
│  │  - /api/health (GET)                             │  │
│  └──────────────┬────────────────────────────────────┘  │
│                 │                                         │
│  ┌──────────────▼──────────────────────────────────┐    │
│  │         Sync Engine (Core Logic)              │    │
│  │  - Dual execution support                     │    │
│  │  - Change detection                           │    │
│  │  - Conflict resolution                        │    │
│  │  - History tracking                           │    │
│  └──────┬────────────────────┬───────────────────┘    │
│         │                    │                          │
│  ┌──────▼────────┐   ┌──────▼──────────┐              │
│  │ Data Loader   │   │  Memory DB      │              │
│  │ - Source      │   │  - Task storage │              │
│  │ - Destination │   │  - Caching      │              │
│  └───────────────┘   └─────────────────┘              │
└─────────────────────────────────────────────────────────┘
                 │
                 │ (Optional)
                 │
┌────────────────▼────────────────────────────────────────┐
│            Background Scheduler (BOT MODE)               │
│  - Runs sync at intervals                                │
│  - Enabled via AUTO_SYNC_ENABLED env var                 │
│  - Configurable interval                                 │
└──────────────────────────────────────────────────────────┘
```

## Execution Modes

### 1. User Tool Mode (Default)
**Who triggers:** Human user

**How it works:**
- User clicks "Sync Now" button in UI
- OR makes direct API call to `/api/sync`
- Backend executes sync immediately
- Returns result to user

**Use cases:**
- Testing
- Demos
- Manual control needed
- Non-technical users
- On-demand sync

**Configuration:**
```env
AUTO_SYNC_ENABLED=False  # Default
```

### 2. Bot Mode (Autonomous)
**Who triggers:** System scheduler

**How it works:**
- Background task starts on app startup
- Runs sync automatically at intervals
- Logs results
- Continues indefinitely

**Use cases:**
- Production deployments
- Continuous synchronization
- No human intervention
- Reliability critical
- 24/7 operation

**Configuration:**
```env
AUTO_SYNC_ENABLED=True
SYNC_INTERVAL_SECONDS=300  # 5 minutes
```

### 3. Hybrid Mode (Both)
Both modes can run simultaneously! Users can:
- Trigger manual syncs anytime
- System auto-syncs in background
- Same sync engine handles both

## Core Components

### 1. Sync Engine (`sync_engine.py`)
**Responsibility:** Core synchronization logic

**Key methods:**
- `sync()` - Main sync operation (used by both modes)
- `dry_run()` - Preview changes without applying
- `get_stats()` - Return current statistics
- `get_history()` - Return sync history

**Algorithm:**
```python
1. Load source tasks
2. Load destination tasks
3. Identify differences:
   - New tasks (add)
   - Changed tasks (update)
   - Unchanged tasks (skip)
4. Push changes to destination
5. Update local database
6. Record sync operation
```

### 2. Data Loader (`data_loader.py`)
**Responsibility:** Interface with external systems

**Current:** Mock implementation for testing
**Future:** Real integrations (Jira, Asana, Trello, etc.)

**Methods:**
- `load_source_tasks()` - Fetch from source
- `load_destination_tasks()` - Fetch from destination
- `push_to_destination()` - Push changes

### 3. Memory DB (`memory_db.py`)
**Responsibility:** Temporary task storage

**Current:** In-memory dictionary
**Future:** PostgreSQL, MongoDB, etc.

**Operations:**
- CRUD operations for tasks
- Local caching
- Fast access

### 4. Routes (`routes/`)
**Responsibility:** HTTP API endpoints

**Endpoints:**
- `POST /api/sync` - Manual sync trigger
- `GET /api/sync/status` - Current status
- `GET /api/sync/history` - Sync history
- `POST /api/sync/dry-run` - Preview changes
- `GET /api/health` - Health check

## Data Flow

### Manual Sync (User Tool Mode)
```
User → Click Button → API Request → Route Handler 
  → Sync Engine → Data Loader → External APIs 
  → Update DB → Return Result → Display to User
```

### Automatic Sync (Bot Mode)
```
Scheduler → Timer Expires → Sync Engine → Data Loader 
  → External APIs → Update DB → Log Result → Wait → Repeat
```

## Configuration

### Environment Variables
```env
# App Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Sync Configuration
AUTO_SYNC_ENABLED=False          # Enable bot mode
SYNC_INTERVAL_SECONDS=300        # 5 minutes

# External Systems (future)
SOURCE_API_URL=https://...
DESTINATION_API_URL=https://...
```

## Extensibility

### Adding New Integrations
1. Extend `DataLoader` class
2. Implement source/destination methods
3. Handle authentication
4. Map to `Task` model

Example:
```python
class JiraDataLoader(DataLoader):
    async def load_source_tasks(self):
        # Implement Jira API call
        pass
```

### Adding New Storage
1. Implement database interface
2. Replace `MemoryDB` with real DB
3. Add migrations
4. Update configuration

### Adding Event-Based Triggers
Instead of time-based (cron), can use:
- Webhooks
- Message queues
- File watchers
- Database triggers

## Scalability

### Current (MVP)
- Single instance
- In-memory storage
- Mock data

### Future
- Multi-instance with load balancer
- Persistent database (PostgreSQL)
- Redis for caching
- Message queue (RabbitMQ/Kafka)
- Kubernetes deployment
- Monitoring (Prometheus/Grafana)

## Security Considerations

### Current
- Basic CORS configuration
- No authentication

### Production Requirements
- API authentication (JWT/OAuth)
- Rate limiting
- Input validation
- Secrets management
- HTTPS only
- Audit logging

## Monitoring & Observability

### Current
- Console logging
- Sync history tracking

### Recommended
- Structured logging (JSON)
- Metrics (sync duration, success rate)
- Alerts (sync failures)
- Dashboards (Grafana)
- Distributed tracing

## Deployment Options

### 1. Local Development
```bash
cd backend
python run.py
```

### 2. Docker
```bash
docker-compose up
```

### 3. Cloud (AWS/GCP/Azure)
- Deploy FastAPI on ECS/Cloud Run
- Use RDS for database
- CloudWatch for monitoring

### 4. Kubernetes
- Deployment for backend
- CronJob for scheduled syncs
- Ingress for routing

## Best Practices

1. **Idempotency** - Same sync multiple times = same result
2. **Error Handling** - Graceful failures, retry logic
3. **Logging** - Comprehensive logs for debugging
4. **Testing** - Unit tests, integration tests
5. **Documentation** - Keep this updated!

## Decision Log

| Decision | Rationale |
|----------|-----------|
| FastAPI | Modern, fast, async support |
| Dual mode | Flexibility for different use cases |
| In-memory DB | MVP simplicity, easy migration later |
| Mock data | Development without external deps |
| Pydantic | Type safety, validation |
