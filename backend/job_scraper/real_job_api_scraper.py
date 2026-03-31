#!/usr/bin/env python3
"""
Real-Time Job API Scraper
Fetches live job data from multiple job board APIs
"""

import requests
import logging
import json
import sqlite3
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional
import time
import re

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealJobAPIScraper:
    """Fetch real-time job data from multiple job board APIs"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(backend_dir, "database", "jobs.db")
        else:
            self.db_path = db_path
        
        # API configurations (add your API keys here)
        self.api_configs = {
            'adzuna': {
                'base_url': 'https://api.adzuna.com/v1/api/jobs',
                'app_id': '09ef4200',
                'app_key': '00e47606f2be07e066bfba71ff97d114',
                'enabled': True  # Now enabled with API keys
            },
            'github_jobs': {
                'base_url': 'https://jobs.github.com/positions.json',
                'enabled': True  # No API key required
            },
            'remotive': {
                'base_url': 'https://remotive.io/api/remote-jobs',
                'enabled': True  # No API key required
            },
            'arbeitnow': {
                'base_url': 'https://www.arbeitnow.com/api/job-board-api',
                'enabled': True  # No API key required
            }
        }
        
        # Target companies and roles
        self.target_companies = [
            'Google', 'Amazon', 'Microsoft', 'Meta', 'Apple', 'Netflix', 'Tesla',
            'OpenAI', 'Anthropic', 'Stripe', 'Airbnb', 'Uber', 'Spotify', 'Adobe'
        ]
        
        self.target_roles = [
            'Software Engineer', 'Frontend Engineer', 'Backend Engineer',
            'Full Stack Engineer', 'Data Scientist', 'ML Engineer', 'AI Engineer',
            'DevOps Engineer', 'Product Manager', 'Data Engineer'
        ]
        
        logger.info("Real-time Job API Scraper initialized")
    
    def fetch_remotive_jobs(self) -> List[Dict]:
        """Fetch jobs from Remotive API"""
        jobs = []
        try:
            logger.info("Fetching jobs from Remotive API...")
            response = requests.get(
                self.api_configs['remotive']['base_url'],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                for job in data.get('jobs', [])[:50]:  # Limit to 50 jobs
                    # Filter by target companies and roles
                    company = job.get('company_name', '')
                    title = job.get('title', '')
                    
                    if self._is_relevant_job(company, title):
                        jobs.append({
                            'company': company,
                            'role': title,
                            'description': job.get('description', ''),
                            'url': job.get('url', ''),
                            'location': job.get('candidate_required_location', 'Remote'),
                            'job_type': job.get('job_type', 'Full-time'),
                            'category': job.get('category', 'Technology'),
                            'publication_date': job.get('publication_date', ''),
                            'source': 'Remotive'
                        })
                
                logger.info(f"Fetched {len(jobs)} relevant jobs from Remotive")
            else:
                logger.warning(f"Remotive API returned status {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching from Remotive: {e}")
        
        return jobs
    
    def fetch_arbeitnow_jobs(self) -> List[Dict]:
        """Fetch jobs from Arbeitnow API"""
        jobs = []
        try:
            logger.info("Fetching jobs from Arbeitnow API...")
            response = requests.get(
                self.api_configs['arbeitnow']['base_url'],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                for job in data.get('data', [])[:50]:
                    company = job.get('company_name', '')
                    title = job.get('title', '')
                    
                    if self._is_relevant_job(company, title):
                        jobs.append({
                            'company': company,
                            'role': title,
                            'description': job.get('description', ''),
                            'url': job.get('url', ''),
                            'location': job.get('location', 'Remote'),
                            'job_type': 'Full-time',
                            'category': job.get('tags', ['Technology'])[0] if job.get('tags') else 'Technology',
                            'publication_date': job.get('created_at', ''),
                            'source': 'Arbeitnow'
                        })
                
                logger.info(f"Fetched {len(jobs)} relevant jobs from Arbeitnow")
            else:
                logger.warning(f"Arbeitnow API returned status {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching from Arbeitnow: {e}")
        
        return jobs
    
    def fetch_adzuna_jobs(self, country: str = 'us') -> List[Dict]:
        """Fetch jobs from Adzuna API (requires API key)"""
        jobs = []
        
        if not self.api_configs['adzuna']['enabled']:
            logger.info("Adzuna API disabled (no API key)")
            return jobs
        
        try:
            logger.info("Fetching jobs from Adzuna API...")
            
            for role in self.target_roles[:5]:  # Limit API calls
                url = f"{self.api_configs['adzuna']['base_url']}/{country}/search/1"
                params = {
                    'app_id': self.api_configs['adzuna']['app_id'],
                    'app_key': self.api_configs['adzuna']['app_key'],
                    'what': role,
                    'results_per_page': 10
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    for job in data.get('results', []):
                        company = job.get('company', {}).get('display_name', 'Unknown')
                        title = job.get('title', '')
                        
                        if self._is_relevant_job(company, title):
                            jobs.append({
                                'company': company,
                                'role': title,
                                'description': job.get('description', ''),
                                'url': job.get('redirect_url', ''),
                                'location': job.get('location', {}).get('display_name', 'Unknown'),
                                'job_type': job.get('contract_type', 'Full-time'),
                                'category': job.get('category', {}).get('label', 'Technology'),
                                'publication_date': job.get('created', ''),
                                'source': 'Adzuna'
                            })
                
                time.sleep(0.5)  # Rate limiting
            
            logger.info(f"Fetched {len(jobs)} relevant jobs from Adzuna")
            
        except Exception as e:
            logger.error(f"Error fetching from Adzuna: {e}")
        
        return jobs
    
    def _is_relevant_job(self, company: str, title: str) -> bool:
        """Check if job is relevant based on company and title"""
        # Check if company matches (case-insensitive, partial match)
        company_match = any(
            target.lower() in company.lower() 
            for target in self.target_companies
        )
        
        # Check if title contains relevant keywords
        title_lower = title.lower()
        role_keywords = [
            'engineer', 'developer', 'scientist', 'analyst', 'manager',
            'architect', 'lead', 'senior', 'junior', 'ml', 'ai', 'data'
        ]
        title_match = any(keyword in title_lower for keyword in role_keywords)
        
        return company_match or title_match
    
    def extract_skills_from_description(self, description: str) -> List[str]:
        """Extract technical skills from job description"""
        skills = []
        
        # Common technical skills to look for
        skill_patterns = [
            # Programming languages
            r'\b(python|java|javascript|typescript|c\+\+|c#|php|ruby|go|swift|kotlin|scala|rust)\b',
            # Web technologies
            r'\b(react|angular|vue|node\.js|express|django|flask|spring|bootstrap)\b',
            # Databases
            r'\b(sql|mysql|postgresql|mongodb|redis|elasticsearch|dynamodb|cassandra)\b',
            # Cloud platforms
            r'\b(aws|azure|gcp|google cloud|docker|kubernetes|jenkins|terraform)\b',
            # Data science
            r'\b(pandas|numpy|scikit-learn|tensorflow|pytorch|keras|spark|hadoop)\b',
            # Tools
            r'\b(git|github|gitlab|jira|confluence|agile|scrum|ci/cd)\b'
        ]
        
        description_lower = description.lower()
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, description_lower, re.IGNORECASE)
            skills.extend(matches)
        
        # Remove duplicates and return
        return list(set(skills))
    
    def extract_experience_requirement(self, description: str) -> str:
        """Extract experience requirement from job description"""
        # Look for patterns like "3+ years", "5-7 years", etc.
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)-(\d+)\s*years?\s*(?:of\s*)?experience',
            r'minimum\s*(?:of\s*)?(\d+)\s*years?',
            r'at\s*least\s*(\d+)\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, description.lower())
            if match:
                if len(match.groups()) == 2:
                    return f"{match.group(1)}-{match.group(2)} years"
                else:
                    return f"{match.group(1)}+ years"
        
        # Default based on title
        title_lower = description.lower()
        if 'senior' in title_lower or 'lead' in title_lower:
            return "5+ years"
        elif 'junior' in title_lower or 'entry' in title_lower:
            return "0-2 years"
        else:
            return "2-5 years"
    
    def extract_education_requirement(self, description: str) -> str:
        """Extract education requirement from job description"""
        description_lower = description.lower()
        
        if 'phd' in description_lower or 'doctorate' in description_lower:
            return "PhD in Computer Science or related field"
        elif 'master' in description_lower or 'ms' in description_lower:
            return "Master's degree in Computer Science or related field"
        elif 'bachelor' in description_lower or 'bs' in description_lower or 'degree' in description_lower:
            return "Bachelor's degree in Computer Science or related field"
        else:
            return "Bachelor's degree preferred"
    
    def save_jobs_to_database(self, jobs: List[Dict]) -> int:
        """Save fetched jobs to database"""
        saved_count = 0
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for job in jobs:
                # Extract job details
                company = job['company']
                role = job['role']
                description = job['description']
                
                # Extract requirements
                skills = self.extract_skills_from_description(description)
                experience = self.extract_experience_requirement(description)
                education = self.extract_education_requirement(description)
                
                # Check if company exists
                cursor.execute("SELECT company_id FROM companies WHERE company_name = ?", (company,))
                result = cursor.fetchone()
                
                if result:
                    company_id = result[0]
                else:
                    # Insert new company
                    cursor.execute("INSERT INTO companies (company_name) VALUES (?)", (company,))
                    company_id = cursor.lastrowid
                
                # Check if job already exists
                cursor.execute("""
                    SELECT job_id FROM job_requirements 
                    WHERE company_id = ? AND role = ?
                """, (company_id, role))
                
                if not cursor.fetchone():
                    # Insert new job
                    cursor.execute("""
                        INSERT INTO job_requirements 
                        (company_id, role, required_skills, tools, experience, education, job_description)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        company_id,
                        role,
                        ', '.join(skills[:10]) if skills else 'Not specified',
                        ', '.join(skills[10:20]) if len(skills) > 10 else 'Not specified',
                        experience,
                        education,
                        description[:500]  # Limit description length
                    ))
                    saved_count += 1
            
            conn.commit()
            conn.close()
            
            logger.info(f"Saved {saved_count} new jobs to database")
            
        except Exception as e:
            logger.error(f"Error saving jobs to database: {e}")
        
        return saved_count
    
    def fetch_all_jobs(self) -> Dict:
        """Fetch jobs from all enabled APIs"""
        all_jobs = []
        stats = {
            'total_fetched': 0,
            'total_saved': 0,
            'sources': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Fetch from Remotive
        if self.api_configs['remotive']['enabled']:
            remotive_jobs = self.fetch_remotive_jobs()
            all_jobs.extend(remotive_jobs)
            stats['sources']['Remotive'] = len(remotive_jobs)
        
        # Fetch from Arbeitnow
        if self.api_configs['arbeitnow']['enabled']:
            arbeitnow_jobs = self.fetch_arbeitnow_jobs()
            all_jobs.extend(arbeitnow_jobs)
            stats['sources']['Arbeitnow'] = len(arbeitnow_jobs)
        
        # Fetch from Adzuna (if enabled)
        if self.api_configs['adzuna']['enabled']:
            adzuna_jobs = self.fetch_adzuna_jobs()
            all_jobs.extend(adzuna_jobs)
            stats['sources']['Adzuna'] = len(adzuna_jobs)
        
        stats['total_fetched'] = len(all_jobs)
        
        # Save to database
        if all_jobs:
            stats['total_saved'] = self.save_jobs_to_database(all_jobs)
        
        return stats
    
    def get_update_status(self) -> Dict:
        """Get status of last job update"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get total companies and jobs
            cursor.execute("SELECT COUNT(*) FROM companies")
            total_companies = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM job_requirements")
            total_jobs = cursor.fetchone()[0]
            
            # Get recent jobs (last 24 hours)
            cursor.execute("""
                SELECT COUNT(*) FROM job_requirements 
                WHERE rowid IN (
                    SELECT rowid FROM job_requirements 
                    ORDER BY rowid DESC LIMIT 100
                )
            """)
            recent_jobs = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_companies': total_companies,
                'total_jobs': total_jobs,
                'recent_jobs': recent_jobs,
                'last_check': datetime.now().isoformat(),
                'apis_enabled': sum(1 for api in self.api_configs.values() if api['enabled'])
            }
            
        except Exception as e:
            logger.error(f"Error getting update status: {e}")
            return {'error': str(e)}

def main():
    """Test the real-time job scraper"""
    scraper = RealJobAPIScraper()
    
    print("=" * 60)
    print("Real-Time Job API Scraper")
    print("=" * 60)
    print()
    
    print("Fetching jobs from APIs...")
    stats = scraper.fetch_all_jobs()
    
    print()
    print("Results:")
    print(f"  Total jobs fetched: {stats['total_fetched']}")
    print(f"  Total jobs saved: {stats['total_saved']}")
    print()
    print("Sources:")
    for source, count in stats['sources'].items():
        print(f"  {source}: {count} jobs")
    print()
    
    status = scraper.get_update_status()
    print("Database Status:")
    print(f"  Total companies: {status['total_companies']}")
    print(f"  Total jobs: {status['total_jobs']}")
    print(f"  APIs enabled: {status['apis_enabled']}")
    print()

if __name__ == "__main__":
    main()