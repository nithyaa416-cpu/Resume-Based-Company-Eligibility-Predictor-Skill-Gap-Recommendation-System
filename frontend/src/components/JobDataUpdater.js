import React, { useState, useEffect } from 'react';

const JobDataUpdater = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [updating, setUpdating] = useState(false);
  const [sources, setSources] = useState([]);
  const [lastUpdate, setLastUpdate] = useState(null);

  // Fetch job status on component mount
  useEffect(() => {
    fetchJobStatus();
    fetchJobSources();
  }, []);

  const fetchJobStatus = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/jobs/status');
      const data = await response.json();
      
      if (data.status === 'success') {
        setStatus(data.data);
        setLastUpdate(new Date(data.data.last_check));
      }
    } catch (error) {
      console.error('Error fetching job status:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchJobSources = async () => {
    try {
      const response = await fetch('http://localhost:5000/jobs/sources');
      const data = await response.json();
      
      if (data.status === 'success') {
        setSources(data.sources);
      }
    } catch (error) {
      console.error('Error fetching job sources:', error);
    }
  };

  const updateJobs = async () => {
    try {
      setUpdating(true);
      const response = await fetch('http://localhost:5000/jobs/fetch-realtime', {
        method: 'POST'
      });
      const data = await response.json();
      
      if (data.status === 'success') {
        alert(`Successfully updated!\n\nFetched: ${data.stats.total_fetched} jobs\nSaved: ${data.stats.total_saved} new jobs\n\nSources:\n${Object.entries(data.stats.sources).map(([source, count]) => `- ${source}: ${count} jobs`).join('\n')}`);
        
        // Refresh status
        fetchJobStatus();
      } else {
        alert('Update failed: ' + data.message);
      }
    } catch (error) {
      console.error('Error updating jobs:', error);
      alert('Error updating jobs. Please try again.');
    } finally {
      setUpdating(false);
    }
  };

  const formatDate = (date) => {
    if (!date) return 'Never';
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getTimeSinceUpdate = () => {
    if (!lastUpdate) return 'Never';
    
    const now = new Date();
    const diff = now - lastUpdate;
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    if (hours > 24) {
      const days = Math.floor(hours / 24);
      return `${days} day${days > 1 ? 's' : ''} ago`;
    } else if (hours > 0) {
      return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else {
      return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    }
  };

  if (loading) {
    return (
      <div className="job-data-updater loading">
        <div className="spinner"></div>
        <p>Loading job data status...</p>
      </div>
    );
  }

  return (
    <div className="job-data-updater">
      <div className="updater-header">
        <h3>📊 Job Database Status</h3>
        <button 
          className="refresh-btn"
          onClick={fetchJobStatus}
          disabled={loading}
        >
          🔄 Refresh
        </button>
      </div>

      {status && (
        <div className="status-grid">
          <div className="status-card">
            <div className="status-value">{status.total_companies}</div>
            <div className="status-label">Companies</div>
          </div>
          
          <div className="status-card">
            <div className="status-value">{status.total_jobs}</div>
            <div className="status-label">Total Jobs</div>
          </div>
          
          <div className="status-card">
            <div className="status-value">{status.recent_jobs}</div>
            <div className="status-label">Recent Jobs</div>
          </div>
          
          <div className="status-card">
            <div className="status-value">{status.apis_enabled}</div>
            <div className="status-label">APIs Enabled</div>
          </div>
        </div>
      )}

      <div className="update-section">
        <div className="update-info">
          <p className="last-update">
            <strong>Last Update:</strong> {formatDate(lastUpdate)}
            <span className="time-ago">({getTimeSinceUpdate()})</span>
          </p>
        </div>
        
        <button 
          className={`update-btn ${updating ? 'updating' : ''}`}
          onClick={updateJobs}
          disabled={updating}
        >
          {updating ? (
            <>
              <span className="spinner-small"></span>
              Fetching Jobs from APIs...
            </>
          ) : (
            <>
              🚀 Update Jobs from APIs
            </>
          )}
        </button>
      </div>

      {sources.length > 0 && (
        <div className="sources-section">
          <h4>Available Job Sources</h4>
          <div className="sources-list">
            {sources.map((source, index) => (
              <div key={index} className={`source-item ${source.enabled ? 'enabled' : 'disabled'}`}>
                <div className="source-name">
                  {source.enabled ? '✅' : '⚠️'} {source.name}
                </div>
                <div className="source-status">
                  {source.enabled ? 'Active' : 'Disabled'}
                  {source.requires_api_key && !source.enabled && ' (API key required)'}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <style jsx>{`
        .job-data-updater {
          background: white;
          border-radius: 12px;
          padding: 24px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
          margin: 20px 0;
        }

        .updater-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
        }

        .updater-header h3 {
          margin: 0;
          color: #333;
          font-size: 20px;
        }

        .refresh-btn {
          background: #f0f0f0;
          border: none;
          padding: 8px 16px;
          border-radius: 6px;
          cursor: pointer;
          font-size: 14px;
          transition: background 0.2s;
        }

        .refresh-btn:hover {
          background: #e0e0e0;
        }

        .status-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 16px;
          margin-bottom: 24px;
        }

        .status-card {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 20px;
          border-radius: 8px;
          text-align: center;
        }

        .status-value {
          font-size: 32px;
          font-weight: bold;
          margin-bottom: 8px;
        }

        .status-label {
          font-size: 14px;
          opacity: 0.9;
        }

        .update-section {
          background: #f8f9fa;
          padding: 20px;
          border-radius: 8px;
          margin-bottom: 20px;
        }

        .update-info {
          margin-bottom: 16px;
        }

        .last-update {
          margin: 0;
          color: #666;
          font-size: 14px;
        }

        .time-ago {
          color: #999;
          margin-left: 8px;
        }

        .update-btn {
          width: 100%;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          padding: 14px 24px;
          border-radius: 8px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: transform 0.2s, box-shadow 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
        }

        .update-btn:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }

        .update-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .update-btn.updating {
          background: #999;
        }

        .sources-section {
          margin-top: 20px;
        }

        .sources-section h4 {
          margin: 0 0 12px 0;
          color: #333;
          font-size: 16px;
        }

        .sources-list {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .source-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 12px;
          border-radius: 6px;
          background: #f8f9fa;
        }

        .source-item.enabled {
          border-left: 3px solid #4caf50;
        }

        .source-item.disabled {
          border-left: 3px solid #ff9800;
          opacity: 0.7;
        }

        .source-name {
          font-weight: 500;
          color: #333;
        }

        .source-status {
          font-size: 12px;
          color: #666;
        }

        .spinner {
          border: 3px solid #f3f3f3;
          border-top: 3px solid #667eea;
          border-radius: 50%;
          width: 40px;
          height: 40px;
          animation: spin 1s linear infinite;
          margin: 20px auto;
        }

        .spinner-small {
          display: inline-block;
          border: 2px solid #ffffff;
          border-top: 2px solid transparent;
          border-radius: 50%;
          width: 16px;
          height: 16px;
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .loading {
          text-align: center;
          padding: 40px;
        }
      `}</style>
    </div>
  );
};

export default JobDataUpdater;