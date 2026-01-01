// Task Sync Engine - Frontend JavaScript

const API_BASE = '/api';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadHealthStatus();
    loadSyncStatus();
    loadSyncHistory();
    
    // Auto-refresh every 30 seconds
    setInterval(() => {
        loadSyncStatus();
        loadSyncHistory();
    }, 30000);
});

// Load health and system info
async function loadHealthStatus() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        updateSystemInfo(data);
        updateModeIndicator(data);
    } catch (error) {
        console.error('Failed to load health status:', error);
        showError('Failed to connect to backend');
    }
}

// Load sync status
async function loadSyncStatus() {
    try {
        const response = await fetch(`${API_BASE}/sync/status`);
        const data = await response.json();
        
        if (data.status === 'ok') {
            updateStatusDisplay(data.stats);
        }
    } catch (error) {
        console.error('Failed to load sync status:', error);
    }
}

// Load sync history
async function loadSyncHistory() {
    try {
        const response = await fetch(`${API_BASE}/sync/history?limit=10`);
        const data = await response.json();
        
        if (data.status === 'ok') {
            displayHistory(data.history);
        }
    } catch (error) {
        console.error('Failed to load sync history:', error);
    }
}

// Trigger manual sync (USER TOOL MODE)
async function triggerSync() {
    const btn = document.getElementById('syncBtn');
    const resultSection = document.getElementById('resultSection');
    const resultDiv = document.getElementById('syncResult');
    
    // Disable button and show loading
    btn.disabled = true;
    btn.innerHTML = '<span class="btn-icon spinning">🔄</span> Syncing...';
    
    try {
        const response = await fetch(`${API_BASE}/sync`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultSection.style.display = 'block';
            resultDiv.className = 'result-box';
            resultDiv.innerHTML = `
                <h3>✅ Sync Successful!</h3>
                <p><strong>Message:</strong> ${data.message}</p>
                <div style="margin-top: 1rem;">
                    <p>📊 <strong>Added:</strong> ${data.stats.added} tasks</p>
                    <p>🔄 <strong>Updated:</strong> ${data.stats.updated} tasks</p>
                    <p>✔️ <strong>Unchanged:</strong> ${data.stats.unchanged} tasks</p>
                    <p>⏱️ <strong>Duration:</strong> ${data.stats.duration_seconds.toFixed(2)}s</p>
                </div>
            `;
            
            // Refresh status and history
            setTimeout(() => {
                loadSyncStatus();
                loadSyncHistory();
            }, 500);
        } else {
            throw new Error(data.message || 'Sync failed');
        }
    } catch (error) {
        resultSection.style.display = 'block';
        resultDiv.className = 'result-box error';
        resultDiv.innerHTML = `
            <h3>❌ Sync Failed</h3>
            <p>${error.message}</p>
        `;
    } finally {
        // Re-enable button
        btn.disabled = false;
        btn.innerHTML = '<span class="btn-icon">🔄</span> Sync Now (User Tool Mode)';
    }
}

// Trigger dry-run sync
async function dryRunSync() {
    const btn = document.getElementById('dryRunBtn');
    const resultSection = document.getElementById('resultSection');
    const resultDiv = document.getElementById('syncResult');
    
    btn.disabled = true;
    btn.innerHTML = '<span class="btn-icon spinning">🔍</span> Running...';
    
    try {
        const response = await fetch(`${API_BASE}/sync/dry-run`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        resultSection.style.display = 'block';
        resultDiv.className = 'result-box';
        resultDiv.innerHTML = `
            <h3>🔍 Dry Run Preview</h3>
            <p><strong>This is a preview - no changes were made</strong></p>
            <div style="margin-top: 1rem;">
                <p>➕ <strong>To Add:</strong> ${data.preview.tasks_to_add.length} tasks</p>
                <p>🔄 <strong>To Update:</strong> ${data.preview.tasks_to_update.length} tasks</p>
                <p>✔️ <strong>Unchanged:</strong> ${data.preview.tasks_unchanged} tasks</p>
                <p>📦 <strong>Source Count:</strong> ${data.source_count}</p>
                <p>📦 <strong>Destination Count:</strong> ${data.destination_count}</p>
            </div>
        `;
    } catch (error) {
        resultSection.style.display = 'block';
        resultDiv.className = 'result-box error';
        resultDiv.innerHTML = `
            <h3>❌ Dry Run Failed</h3>
            <p>${error.message}</p>
        `;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<span class="btn-icon">🔍</span> Dry Run';
    }
}

// Refresh status manually
async function refreshStatus() {
    const btn = document.getElementById('refreshBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="btn-icon spinning">🔃</span> Refreshing...';
    
    await Promise.all([
        loadHealthStatus(),
        loadSyncStatus(),
        loadSyncHistory()
    ]);
    
    btn.disabled = false;
    btn.innerHTML = '<span class="btn-icon">🔃</span> Refresh Status';
}

// Update system info display
function updateSystemInfo(data) {
    document.getElementById('appName').textContent = data.app_name;
    document.getElementById('version').textContent = data.version;
    document.getElementById('mode').textContent = data.mode;
    document.getElementById('syncInterval').textContent = 
        `${data.sync_interval_seconds} seconds`;
    document.getElementById('autoSyncStatus').textContent = 
        data.auto_sync_enabled ? '✅ Enabled' : '❌ Disabled';
}

// Update mode indicator
function updateModeIndicator(data) {
    const badge = document.getElementById('modeBadge');
    const icon = document.getElementById('modeIcon');
    const text = document.getElementById('modeText');
    
    if (data.auto_sync_enabled) {
        badge.className = 'mode-badge bot-mode';
        icon.textContent = '🤖';
        text.textContent = 'Bot Mode + User Tool';
    } else {
        badge.className = 'mode-badge tool-mode';
        icon.textContent = '🔧';
        text.textContent = 'User Tool Mode';
    }
}

// Update status display
function updateStatusDisplay(stats) {
    document.getElementById('totalSyncs').textContent = stats.total_syncs || 0;
    document.getElementById('tasksCount').textContent = stats.tasks_in_db || 0;
    
    if (stats.last_sync_time) {
        const date = new Date(stats.last_sync_time);
        document.getElementById('lastSync').textContent = date.toLocaleString();
    } else {
        document.getElementById('lastSync').textContent = 'Never';
    }
}

// Display sync history
function displayHistory(history) {
    const container = document.getElementById('historyContainer');
    
    if (!history || history.length === 0) {
        container.innerHTML = '<p class="empty-state">No sync history yet. Click "Sync Now" to start!</p>';
        return;
    }
    
    container.innerHTML = history.reverse().map(record => {
        const success = record.success !== false;
        const date = new Date(record.timestamp);
        
        if (record.error) {
            return `
                <div class="history-item error">
                    <div class="history-timestamp">❌ ${date.toLocaleString()}</div>
                    <p style="color: var(--error-color);"><strong>Error:</strong> ${record.error}</p>
                </div>
            `;
        }
        
        return `
            <div class="history-item success">
                <div class="history-timestamp">✅ ${date.toLocaleString()}</div>
                <div class="history-stats">
                    <span>📊 Source: ${record.source_count || 0}</span>
                    <span>📦 Dest: ${record.destination_count || 0}</span>
                    <span>➕ Added: ${record.added || 0}</span>
                    <span>🔄 Updated: ${record.updated || 0}</span>
                    <span>⏱️ ${record.duration_seconds?.toFixed(2) || 0}s</span>
                </div>
            </div>
        `;
    }).join('');
}

// Show error notification
function showError(message) {
    const resultSection = document.getElementById('resultSection');
    const resultDiv = document.getElementById('syncResult');
    
    resultSection.style.display = 'block';
    resultDiv.className = 'result-box error';
    resultDiv.innerHTML = `<h3>❌ Error</h3><p>${message}</p>`;
}
