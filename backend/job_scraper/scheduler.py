#!/usr/bin/env python3
"""
Job Data Scheduler
Automatically updates job data at regular intervals
"""

import schedule
import time
import logging
from datetime import datetime
from real_time_scraper import RealTimeJobScraper
import threading
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobDataScheduler:
    """Scheduler for automatic job data updates"""
    
    def __init__(self):
        self.scraper = RealTimeJobScraper()
        self.is_running = False
        self.last_update = None
        self.update_stats = {}
        
    def update_job_data(self):
        """Update job data and log results"""
        try:
            logger.info("🔄 Starting scheduled job data update...")
            
            results = self.scraper.run_real_time_update()
            
            self.last_update = datetime.now().isoformat()
            self.update_stats = results
            
            # Log summary
            logger.info(f"✅ Scheduled update completed:")
            logger.info(f"   📊 Total scraped: {results.get('total_scraped', 0)}")
            logger.info(f"   💾 New jobs saved: {results.get('total_saved', 0)}")
            logger.info(f"   🕐 Last update: {self.last_update}")
            
            # Save update log
            self._save_update_log(results)
            
        except Exception as e:
            logger.error(f"❌ Scheduled update failed: {e}")
    
    def _save_update_log(self, results: dict):
        """Save update log to file"""
        try:
            log_entry = {
                "timestamp": self.last_update,
                "results": results
            }
            
            log_file = "job_update_log.json"
            
            # Load existing log
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {"updates": []}
            
            # Add new entry
            log_data["updates"].append(log_entry)
            
            # Keep only last 50 entries
            log_data["updates"] = log_data["updates"][-50:]
            
            # Save updated log
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving update log: {e}")
    
    def start_scheduler(self):
        """Start the job scheduler"""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        logger.info("🚀 Starting job data scheduler...")
        
        # Schedule updates
        schedule.every(6).hours.do(self.update_job_data)  # Every 6 hours
        schedule.every().day.at("09:00").do(self.update_job_data)  # Daily at 9 AM
        schedule.every().monday.at("08:00").do(self.update_job_data)  # Weekly on Monday
        
        # Run initial update
        self.update_job_data()
        
        self.is_running = True
        
        # Run scheduler in background thread
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        logger.info("✅ Job scheduler started successfully")
        logger.info("📅 Schedule: Every 6 hours, Daily at 9 AM, Weekly on Monday")
    
    def stop_scheduler(self):
        """Stop the job scheduler"""
        self.is_running = False
        schedule.clear()
        logger.info("🛑 Job scheduler stopped")
    
    def get_status(self) -> dict:
        """Get scheduler status"""
        return {
            "is_running": self.is_running,
            "last_update": self.last_update,
            "update_stats": self.update_stats,
            "next_run": str(schedule.next_run()) if schedule.jobs else None
        }
    
    def force_update(self) -> dict:
        """Force an immediate update"""
        logger.info("🔄 Forcing immediate job data update...")
        self.update_job_data()
        return self.update_stats

# Global scheduler instance
job_scheduler = JobDataScheduler()

def start_background_scheduler():
    """Start the background job scheduler"""
    job_scheduler.start_scheduler()

def get_scheduler_status():
    """Get current scheduler status"""
    return job_scheduler.get_status()

def force_job_update():
    """Force an immediate job update"""
    return job_scheduler.force_update()

if __name__ == "__main__":
    # Run scheduler as standalone script
    scheduler = JobDataScheduler()
    
    try:
        scheduler.start_scheduler()
        logger.info("🔄 Scheduler running... Press Ctrl+C to stop")
        
        # Keep the script running
        while True:
            time.sleep(10)
            
    except KeyboardInterrupt:
        logger.info("🛑 Stopping scheduler...")
        scheduler.stop_scheduler()
        logger.info("✅ Scheduler stopped successfully")