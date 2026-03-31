# Real-Time Job API Setup Guide

## 🚀 Overview

The system now supports real-time job updates from multiple job board APIs:

- **Remotive** - Remote job listings (No API key required)
- **Arbeitnow** - European job board (No API key required)
- **Adzuna** - Global job search (Requires free API key)
- **GitHub Jobs** - Tech jobs (No API key required - deprecated but still works)

## 📋 Quick Start

### 1. Install Required Dependencies

```bash
cd resume/backend
pip install requests schedule
```

Or add to your virtual environment:
```bash
.\venv_py310\Scripts\pip.exe install requests schedule
```

### 2. Test the Job Scraper

```bash
python job_scraper/real_job_api_scraper.py
```

This will:
- Fetch jobs from enabled APIs
- Extract skills, experience, and education requirements
- Save relevant jobs to the database
- Display statistics

### 3. Use the API Endpoints

Start your Flask server and use these endpoints:

#### Fetch Real-Time Jobs
```bash
POST http://localhost:5000/jobs/fetch-realtime
```

Response:
```json
{
  "status": "success",
  "message": "Real-time job data fetched successfully",
  "stats": {
    "total_fetched": 45,
    "total_saved": 32,
    "sources": {
      "Remotive": 25,
      "Arbeitnow": 20
    },
    "timestamp": "2026-02-22T10:30:00"
  }
}
```

#### Get Job Database Status
```bash
GET http://localhost:5000/jobs/status
```

Response:
```json
{
  "status": "success",
  "data": {
    "total_companies": 45,
    "total_jobs": 150,
    "recent_jobs": 32,
    "last_check": "2026-02-22T10:30:00",
    "apis_enabled": 2
  }
}
```

#### Get Available Job Sources
```bash
GET http://localhost:5000/jobs/sources
```

Response:
```json
{
  "status": "success",
  "sources": [
    {
      "name": "Remotive",
      "enabled": true,
      "requires_api_key": false,
      "base_url": "https://remotive.io/api/remote-jobs"
    },
    {
      "name": "Adzuna",
      "enabled": false,
      "requires_api_key": true,
      "base_url": "https://api.adzuna.com/v1/api/jobs"
    }
  ],
  "total_enabled": 2
}
```

## 🔑 API Key Setup (Optional)

### Adzuna API (Recommended for more jobs)

1. **Sign up for free API key:**
   - Visit: https://developer.adzuna.com/
   - Create account
   - Get your App ID and App Key

2. **Set environment variables:**

   **Windows:**
   ```cmd
   set ADZUNA_APP_ID=your_app_id_here
   set ADZUNA_APP_KEY=your_app_key_here
   ```

   **Linux/Mac:**
   ```bash
   export ADZUNA_APP_ID=your_app_id_here
   export ADZUNA_APP_KEY=your_app_key_here
   ```

3. **Enable in code:**
   Edit `job_scraper/real_job_api_scraper.py`:
   ```python
   'adzuna': {
       'base_url': 'https://api.adzuna.com/v1/api/jobs',
       'app_id': os.environ.get('ADZUNA_APP_ID', 'YOUR_APP_ID'),
       'app_key': os.environ.get('ADZUNA_APP_KEY', 'YOUR_APP_KEY'),
       'enabled': True  # Change to True
   }
   ```

## ⏰ Automatic Updates

### Option 1: Manual Scheduling (Simple)

Run the auto-updater in a separate terminal:

```bash
cd resume/backend
python job_scraper/auto_job_updater.py --interval 24
```

This will:
- Update jobs every 24 hours
- Run continuously in the background
- Log all updates

### Option 2: Run Once

```bash
python job_scraper/auto_job_updater.py --once
```

### Option 3: Windows Task Scheduler

1. Create a batch file `update_jobs.bat`:
```batch
@echo off
cd D:\path\to\resume\backend
.\venv_py310\Scripts\python.exe job_scraper/auto_job_updater.py --once
```

2. Open Task Scheduler
3. Create Basic Task
4. Set trigger (e.g., Daily at 2 AM)
5. Action: Start a program
6. Program: `update_jobs.bat`

### Option 4: Linux Cron Job

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * cd /path/to/resume/backend && ./venv_py310/bin/python job_scraper/auto_job_updater.py --once
```

## 🎯 Customization

### Target Specific Companies

Edit `real_job_api_scraper.py`:

```python
self.target_companies = [
    'Google', 'Amazon', 'Microsoft', 'Meta', 'Apple',
    'Your', 'Custom', 'Companies', 'Here'
]
```

### Target Specific Roles

```python
self.target_roles = [
    'Software Engineer', 'Data Scientist',
    'Your', 'Custom', 'Roles', 'Here'
]
```

### Add More APIs

Add new API configuration:

```python
'your_api': {
    'base_url': 'https://api.example.com/jobs',
    'api_key': os.environ.get('YOUR_API_KEY'),
    'enabled': True
}
```

Then implement the fetch method:

```python
def fetch_your_api_jobs(self) -> List[Dict]:
    """Fetch jobs from Your API"""
    jobs = []
    # Your implementation here
    return jobs
```

## 📊 Features

### Automatic Skill Extraction

The scraper automatically extracts:
- Programming languages (Python, Java, JavaScript, etc.)
- Web technologies (React, Angular, Node.js, etc.)
- Databases (MySQL, MongoDB, PostgreSQL, etc.)
- Cloud platforms (AWS, Azure, GCP, etc.)
- Data science tools (Pandas, TensorFlow, PyTorch, etc.)

### Experience Level Detection

Automatically detects:
- "3+ years experience"
- "5-7 years experience"
- "Senior" → 5+ years
- "Junior" → 0-2 years

### Education Requirements

Extracts:
- PhD requirements
- Master's degree requirements
- Bachelor's degree requirements

## 🔧 Troubleshooting

### Issue: No jobs fetched

**Solution:**
1. Check internet connection
2. Verify API endpoints are accessible
3. Check API rate limits
4. Enable more job sources

### Issue: API key errors

**Solution:**
1. Verify environment variables are set
2. Check API key is valid
3. Ensure API key has correct permissions

### Issue: Database errors

**Solution:**
1. Check database file exists: `database/jobs.db`
2. Verify write permissions
3. Run database creation script if needed

### Issue: Too many duplicate jobs

**Solution:**
The scraper checks for duplicates before inserting. If you see duplicates:
1. Clear old jobs: `DELETE FROM job_requirements WHERE rowid < X`
2. Adjust relevance filters in `_is_relevant_job()`

## 📈 Performance Tips

### Rate Limiting

The scraper includes automatic rate limiting:
- 0.5 second delay between API calls
- Limits results per API (50 jobs max)
- Respects API terms of service

### Optimize Database

```sql
-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_company_name ON companies(company_name);
CREATE INDEX IF NOT EXISTS idx_job_role ON job_requirements(role);
CREATE INDEX IF NOT EXISTS idx_company_id ON job_requirements(company_id);
```

### Reduce API Calls

1. Increase update interval (24-48 hours)
2. Limit target companies/roles
3. Cache results locally

## 🌐 Frontend Integration

### Update Frontend to Show Real-Time Status

Add to your frontend:

```javascript
// Fetch real-time jobs
async function fetchRealtimeJobs() {
  const response = await fetch('http://localhost:5000/jobs/fetch-realtime', {
    method: 'POST'
  });
  const data = await response.json();
  console.log('Jobs updated:', data.stats);
}

// Get job status
async function getJobStatus() {
  const response = await fetch('http://localhost:5000/jobs/status');
  const data = await response.json();
  console.log('Job database status:', data.data);
}

// Show update button
<button onclick="fetchRealtimeJobs()">
  Update Jobs from APIs
</button>
```

### Display Last Update Time

```javascript
async function displayJobStatus() {
  const response = await fetch('http://localhost:5000/jobs/status');
  const data = await response.json();
  
  document.getElementById('job-count').textContent = data.data.total_jobs;
  document.getElementById('last-update').textContent = 
    new Date(data.data.last_check).toLocaleString();
}
```

## 📝 API Response Examples

### Successful Job Fetch

```json
{
  "status": "success",
  "stats": {
    "total_fetched": 45,
    "total_saved": 32,
    "sources": {
      "Remotive": 25,
      "Arbeitnow": 20
    },
    "timestamp": "2026-02-22T10:30:00"
  }
}
```

### Job Status

```json
{
  "status": "success",
  "data": {
    "total_companies": 45,
    "total_jobs": 150,
    "recent_jobs": 32,
    "last_check": "2026-02-22T10:30:00",
    "apis_enabled": 2
  }
}
```

## 🚀 Next Steps

1. **Test the scraper:**
   ```bash
   python job_scraper/real_job_api_scraper.py
   ```

2. **Set up automatic updates:**
   ```bash
   python job_scraper/auto_job_updater.py --interval 24
   ```

3. **Get API keys** (optional but recommended):
   - Adzuna: https://developer.adzuna.com/

4. **Integrate with frontend:**
   - Add "Update Jobs" button
   - Display last update time
   - Show job count statistics

5. **Monitor and optimize:**
   - Check logs for errors
   - Adjust target companies/roles
   - Fine-tune relevance filters

## 📚 Additional Resources

- Remotive API: https://remotive.io/api-documentation
- Arbeitnow API: https://www.arbeitnow.com/api
- Adzuna API: https://developer.adzuna.com/docs
- Schedule library: https://schedule.readthedocs.io/

## 🎉 Benefits

✅ **Real-time job data** - Always up-to-date job listings
✅ **Multiple sources** - Aggregate from multiple job boards
✅ **Automatic extraction** - Skills, experience, education auto-detected
✅ **No manual updates** - Set it and forget it
✅ **Customizable** - Target specific companies and roles
✅ **Free to use** - Most APIs don't require keys
✅ **Scalable** - Easy to add more job sources