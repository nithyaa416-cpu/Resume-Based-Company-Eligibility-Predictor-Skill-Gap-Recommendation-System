#!/usr/bin/env python3
"""
Automatic Job Updater with Scheduler
Periodically fetches and updates job data from APIs
"""

import schedule
import time
import logging
from datetime import datetime
from real_job_api_scraper import RealJobAPIScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AutoJobUpdater:
    """Automatic job updater with scheduling"""
    
    def __init__(self, update_interval_hours: int = 24):
        self.scraper = RealJobAPIScraper()
        self.update_interval_hours = update_interval_hours
        self.last_update = None
        self.update_count = 0
        
        logger.info(f"Auto Job Updater initialized (interval: {update_interval_hours} hours)")
    
    def update_jobs(self):
        """Fetch and update jobs from APIs"""
        try:
            logger.info("=" * 60)
            logger.info(f"Starting automatic job update #{self.update_count + 1}")
            logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info("=" * 60)
            
            # Fetch jobs
            stats = self.scraper.fetch_all_jobs()
            
            # Update tracking
            self.last_update = datetime.now()
            self.update_count += 1
            
            # Log results
            logger.info(f"Update completed successfully!")
            logger.info(f"  Jobs fetched: {stats['total_fetched']}")
            logger.info(f"  Jobs saved: {stats['total_saved']}")
            logger.info(f"  Sources used: {len(stats['sources'])}")
            
            for source, count in stats['sources'].items():
                logger.info(f"    - {source}: {count} jobs")
            
            logger.info(f"  Next update in {self.update_interval_hours} hours")
            logger.info("=" * 60)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error during automatic update: {e}")
            return None
    
    def start_scheduler(self):
        """Start the automatic update scheduler"""
        logger.info("Starting job update scheduler...")
        logger.info(f"Updates will run every {self.update_interval_hours} hours")
        
        # Schedule the job
        schedule.every(self.update_interval_hours).hours.do(self.update_jobs)
        
        # Run immediately on start
        logger.info("Running initial update...")
        self.update_jobs()
        
        # Keep running
        logger.info("Scheduler is now running. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
    
    def get_status(self) -> dict:
        """Get current status of the updater"""
        return {
            'update_count': self.update_count,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'update_interval_hours': self.update_interval_hours,
            'next_update': schedule.next_run().isoformat() if schedule.jobs else None
        }

def main():
    """Run the automatic job updater"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Automatic Job Updater')
    parser.add_argument(
        '--interval',
        type=int,
        default=24,
        help='Update interval in hours (default: 24)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (no scheduling)'
    )
    
    args = parser.parse_args()
    
    updater = AutoJobUpdater(update_interval_hours=args.interval)
    
    if args.once:
        logger.info("Running single update...")
        updater.update_jobs()
        logger.info("Update complete. Exiting.")
    else:
        updater.start_scheduler()

if __name__ == "__main__":
    main()