# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently no authentication (add in production).

---

## Endpoints

### 1. Health Check

Check if the service is running and get system information.

**Endpoint:** `GET /api/health`

**Request:**
```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Task Sync Engine",
  "version": "1.0.0",
  "timestamp": "2026-01-01T10:30:00",
  "mode": "bot + user-tool",
  "auto_sync_enabled": true,
  "sync_interval_seconds": 300
}
```

---

### 2. Trigger Manual Sync (User Tool Mode)

Manually trigger a synchronization operation.

**Endpoint:** `POST /api/sync`

**Request:**
```bash
curl -X POST http://localhost:8000/api/sync
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Sync completed successfully",
  "stats": {
    "timestamp": "2026-01-01T10:35:00",
    "duration_seconds": 1.23,
    "source_count": 5,
    "destination_count": 3,
    "added": 2,
    "updated": 1,
    "unchanged": 2,
    "success": true
  }
}
```

**Response (Error):**
```json
{
  "detail": "Error message here"
}
```

**Status Codes:**
- `200` - Sync successful
- `500` - Sync failed

---

### 3. Get Sync Status

Get current synchronization statistics.

**Endpoint:** `GET /api/sync/status`

**Request:**
```bash
curl http://localhost:8000/api/sync/status
```

**Response:**
```json
{
  "status": "ok",
  "stats": {
    "total_syncs": 15,
    "last_sync_time": "2026-01-01T10:35:00",
    "tasks_in_db": 8
  },
  "timestamp": "2026-01-01T10:40:00"
}
```

---

### 4. Get Sync History

Retrieve recent synchronization history.

**Endpoint:** `GET /api/sync/history`

**Query Parameters:**
- `limit` (optional, default=10) - Number of records to return

**Request:**
```bash
curl http://localhost:8000/api/sync/history?limit=5
```

**Response:**
```json
{
  "status": "ok",
  "history": [
    {
      "timestamp": "2026-01-01T10:35:00",
      "duration_seconds": 1.23,
      "source_count": 5,
      "destination_count": 3,
      "added": 2,
      "updated": 1,
      "unchanged": 2,
      "success": true
    },
    {
      "timestamp": "2026-01-01T10:30:00",
      "error": "Connection timeout",
      "success": false
    }
  ],
  "count": 2
}
```

---

### 5. Dry Run Sync

Preview what would be synchronized without making changes.

**Endpoint:** `POST /api/sync/dry-run`

**Request:**
```bash
curl -X POST http://localhost:8000/api/sync/dry-run
```

**Response:**
```json
{
  "dry_run": true,
  "preview": {
    "tasks_to_add": [
      {
        "id": "task-1",
        "title": "New Task",
        "description": "Task description",
        "status": "todo",
        "priority": "high",
        "assignee": null,
        "tags": [],
        "created_at": "2026-01-01T10:00:00",
        "updated_at": "2026-01-01T10:00:00"
      }
    ],
    "tasks_to_update": [
      {
        "id": "task-2",
        "title": "Updated Task",
        "status": "in_progress",
        "priority": "medium"
      }
    ],
    "tasks_unchanged": 3
  },
  "source_count": 5,
  "destination_count": 4
}
```

---

## Data Models

### Task Model

```json
{
  "id": "string",              // Unique identifier
  "title": "string",           // Task title (required)
  "description": "string",     // Task description (optional)
  "status": "string",          // todo | in_progress | done | blocked
  "priority": "string",        // low | medium | high | urgent
  "assignee": "string",        // Assigned person (optional)
  "tags": ["string"],          // Array of tags
  "created_at": "datetime",    // ISO 8601 timestamp
  "updated_at": "datetime"     // ISO 8601 timestamp
}
```

**Example:**
```json
{
  "id": "task-123",
  "title": "Implement authentication",
  "description": "Add OAuth2 to the API",
  "status": "in_progress",
  "priority": "high",
  "assignee": "john@example.com",
  "tags": ["backend", "security"],
  "created_at": "2026-01-01T09:00:00",
  "updated_at": "2026-01-01T10:00:00"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error description"
}
```

**Common Status Codes:**
- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

---

## Usage Examples

### Python
```python
import requests

# Health check
response = requests.get('http://localhost:8000/api/health')
print(response.json())

# Trigger sync
response = requests.post('http://localhost:8000/api/sync')
result = response.json()
print(f"Sync completed: {result['success']}")
print(f"Added: {result['stats']['added']}")
print(f"Updated: {result['stats']['updated']}")
```

### JavaScript
```javascript
// Trigger sync
fetch('http://localhost:8000/api/sync', {
  method: 'POST'
})
  .then(response => response.json())
  .then(data => {
    console.log('Sync completed:', data.success);
    console.log('Stats:', data.stats);
  });

// Get sync history
fetch('http://localhost:8000/api/sync/history?limit=5')
  .then(response => response.json())
  .then(data => {
    console.log('History:', data.history);
  });
```

### cURL
```bash
# Health check
curl http://localhost:8000/api/health

# Trigger sync
curl -X POST http://localhost:8000/api/sync

# Get status
curl http://localhost:8000/api/sync/status

# Get history
curl http://localhost:8000/api/sync/history?limit=10

# Dry run
curl -X POST http://localhost:8000/api/sync/dry-run
```

---

## Rate Limiting

Currently no rate limiting (add in production).

**Recommended for production:**
- 100 requests per minute per IP
- Implement using `slowapi` or similar

---

## Webhooks (Future)

Support for webhooks to notify external systems:

```json
POST /api/webhooks/register
{
  "url": "https://your-app.com/webhook",
  "events": ["sync.completed", "sync.failed"]
}
```

---

## Pagination (Future)

For large datasets:
```
GET /api/sync/history?page=1&per_page=20
```

---

## Filtering (Future)

Filter sync history:
```
GET /api/sync/history?status=success&from=2026-01-01&to=2026-01-31
```

---

## WebSocket Support (Future)

Real-time sync status updates:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/sync-status');
ws.onmessage = (event) => {
  console.log('Sync update:', JSON.parse(event.data));
};
```

---

## API Versioning

Current: v1 (implicit)

Future versions:
```
/api/v2/sync
```

---

## OpenAPI/Swagger

Interactive API documentation available at:
```
http://localhost:8000/docs
```

Alternative ReDoc UI:
```
http://localhost:8000/redoc
```
