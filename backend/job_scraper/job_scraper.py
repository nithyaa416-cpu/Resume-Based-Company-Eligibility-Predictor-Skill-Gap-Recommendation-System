#!/usr/bin/env python3
"""
Real-time Job Scraper for AI Resume Analyzer
Fetches live job postings from multiple sources
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sqlite3
import os
from dataclasses import dataclass
from urllib.parse import urlencode, quote_plus
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class JobPosting:
    """Data class for job posting information"""
    company: str
    role: str
    location: str
    required_skills: str
    tools: str
    experience: str
    education: str
    job_description: str
    salary_range: str
    job_type: str  # Full-time, Part-time, Contract
    remote_option: str  # Remote, Hybrid, On-site
    posted_date: str
    source_url: str
    source_platform: str

class JobScraper:
    """Main job scraper class"""
    
    def __init__(self, db_path: str = "../database/jobs.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def scrape_adzuna_jobs(self, keywords: List[str], locations: List[str], limit: int = 50) -> List[JobPosting]:
        """
        Scrape jobs from Adzuna API (free tier available)
        """
        jobs = []
        
        # Adzuna API (requires free API key)
        app_id = "your_adzuna_app_id"  # Get from https://developer.adzuna.com/
        app_key = "your_adzuna_app_key"
        
        for keyword in keywords:
            for location in locations:
                try:
                    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"
                    params = {
                        'app_id': app_id,
                        'app_key': app_key,
                        'what': keyword,
                        'where': location,
                        'results_per_page': min(limit, 50),
                        'sort_by': 'date'
                    }
                    
                    response = self.session.get(url, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        
                        for job in data.get('results', []):
                            job_posting = self._parse_adzuna_job(job)
                            if job_posting:
                                jobs.append(job_posting)
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"Error scraping Adzuna for {keyword} in {location}: {e}")
                    
        return jobs
    
    def scrape_github_jobs(self, keywords: List[str], limit: int = 50) -> List[JobPosting]:
        """
        Scrape tech jobs from GitHub Jobs API (if available) or similar tech job boards
        """
        jobs = []
        
        # Since GitHub Jobs API is deprecated, we'll use a different approach
        # This is a placeholder for other tech job APIs like:
        # - RemoteOK API
        # - AngelList API
        # - Stack Overflow Jobs API
        
        try:
            # Example: RemoteOK API (free)
            url = "https://remoteok.io/api"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                for job in data[1:limit+1]:  # Skip first element (metadata)
                    if any(keyword.lower() in job.get('tags', []) for keyword in keywords):
                        job_posting = self._parse_remoteok_job(job)
                        if job_posting:
                            jobs.append(job_posting)
                            
        except Exception as e:
            logger.error(f"Error scraping RemoteOK: {e}")
            
        return jobs
    
    def scrape_indeed_jobs(self, keywords: List[str], locations: List[str], limit: int = 50) -> List[JobPosting]:
        """
        Scrape jobs from Indeed (web scraping - be respectful of rate limits)
        """
        jobs = []
        
        for keyword in keywords:
            for location in locations:
                try:
                    # Indeed search URL
                    params = {
                        'q': keyword,
                        'l': location,
                        'sort': 'date',
                        'limit': min(limit, 50)
                    }
                    
                    url = f"https://www.indeed.com/jobs?{urlencode(params)}"
                    
                    # Add delay to be respectful
                    time.sleep(2)
                    
                    response = self.session.get(url)
                    if response.status_code == 200:
                        # Parse HTML response (simplified - would need BeautifulSoup)
                        job_postings = self._parse_indeed_html(response.text, keyword, location)
                        jobs.extend(job_postings)
                        
                except Exception as e:
                    logger.error(f"Error scraping Indeed for {keyword} in {location}: {e}")
                    
        return jobs
    
    def scrape_linkedin_jobs(self, keywords: List[str], locations: List[str], limit: int = 50) -> List[JobPosting]:
        """
        Scrape jobs from LinkedIn (requires LinkedIn API access or web scraping)
        """
        jobs = []
        
        # LinkedIn requires authentication and has strict rate limits
        # This would need LinkedIn API credentials or careful web scraping
        
        logger.info("LinkedIn scraping requires API access - implementing placeholder")
        
        return jobs
    
    def _parse_adzuna_job(self, job_data: Dict) -> Optional[JobPosting]:
        """Parse Adzuna job data into JobPosting object"""
        try:
            # Extract skills from description using NLP
            description = job_data.get('description', '')
            skills = self._extract_skills_from_description(description)
            
            return JobPosting(
                company=job_data.get('company', {}).get('display_name', 'Unknown'),
                role=job_data.get('title', 'Unknown Role'),
                location=job_data.get('location', {}).get('display_name', 'Unknown'),
                required_skills=', '.join(skills.get('technical', [])),
                tools=', '.join(skills.get('tools', [])),
                experience=self._extract_experience_from_description(description),
                education=self._extract_education_from_description(description),
                job_description=description[:500] + '...' if len(description) > 500 else description,
                salary_range=f"${job_data.get('salary_min', 0)}-${job_data.get('salary_max', 0)}" if job_data.get('salary_min') else 'Not specified',
                job_type='Full-time',  # Default
                remote_option='On-site',  # Default
                posted_date=job_data.get('created', ''),
                source_url=job_data.get('redirect_url', ''),
                source_platform='Adzuna'
            )
        except Exception as e:
            logger.error(f"Error parsing Adzuna job: {e}")
            return None
    
    def _parse_remoteok_job(self, job_data: Dict) -> Optional[JobPosting]:
        """Parse RemoteOK job data into JobPosting object"""
        try:
            description = job_data.get('description', '')
            tags = job_data.get('tags', [])
            
            # Separate technical skills from tools
            technical_skills = [tag for tag in tags if tag.lower() in [
                'python', 'javascript', 'react', 'node', 'java', 'c++', 'go', 'rust',
                'machine learning', 'ai', 'data science', 'sql', 'mongodb'
            ]]
            
            tools = [tag for tag in tags if tag.lower() in [
                'docker', 'kubernetes', 'aws', 'gcp', 'azure', 'git', 'jenkins'
            ]]
            
            return JobPosting(
                company=job_data.get('company', 'Unknown'),
                role=job_data.get('position', 'Unknown Role'),
                location='Remote',
                required_skills=', '.join(technical_skills),
                tools=', '.join(tools),
                experience=self._extract_experience_from_description(description),
                education=self._extract_education_from_description(description),
                job_description=description[:500] + '...' if len(description) > 500 else description,
                salary_range=f"${job_data.get('salary_min', 0)}-${job_data.get('salary_max', 0)}" if job_data.get('salary_min') else 'Not specified',
                job_type='Full-time',
                remote_option='Remote',
                posted_date=datetime.fromtimestamp(job_data.get('date', 0)).isoformat(),
                source_url=job_data.get('url', ''),
                source_platform='RemoteOK'
            )
        except Exception as e:
            logger.error(f"Error parsing RemoteOK job: {e}")
            return None
    
    def _extract_skills_from_description(self, description: str) -> Dict[str, List[str]]:
        """Extract technical skills and tools from job description using regex"""
        
        # Common technical skills
        technical_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Go', 'Rust', 'PHP', 'Ruby',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring',
            'Machine Learning', 'AI', 'Data Science', 'Deep Learning', 'NLP',
            'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
            'HTML', 'CSS', 'TypeScript', 'GraphQL', 'REST API'
        ]
        
        # Common tools and platforms
        tools = [
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Git', 'Jenkins',
            'Terraform', 'Ansible', 'Linux', 'Windows', 'MacOS',
            'Jira', 'Confluence', 'Slack', 'Teams'
        ]
        
        found_skills = {'technical': [], 'tools': []}
        
        description_lower = description.lower()
        
        for skill in technical_skills:
            if skill.lower() in description_lower:
                found_skills['technical'].append(skill)
                
        for tool in tools:
            if tool.lower() in description_lower:
                found_skills['tools'].append(tool)
                
        return found_skills
    
    def _extract_experience_from_description(self, description: str) -> str:
        """Extract experience requirements from job description"""
        experience_patterns = [
            r'(\d+)[\+\-\s]*years?\s+(?:of\s+)?experience',
            r'(\d+)[\+\-\s]*yrs?\s+(?:of\s+)?experience',
            r'minimum\s+(\d+)\s+years?',
            r'at least\s+(\d+)\s+years?'
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, description.lower())
            if match:
                years = match.group(1)
                return f"{years}+ years"
                
        # Check for entry level indicators
        entry_level_keywords = ['entry level', 'junior', 'graduate', 'new grad', 'fresh']
        if any(keyword in description.lower() for keyword in entry_level_keywords):
            return "0-2 years"
            
        return "Not specified"
    
    def _extract_education_from_description(self, description: str) -> str:
        """Extract education requirements from job description"""
        education_patterns = [
            r'bachelor[\'s]*\s+degree',
            r'master[\'s]*\s+degree',
            r'phd|doctorate',
            r'computer science|cs degree',
            r'engineering degree'
        ]
        
        description_lower = description.lower()
        
        for pattern in education_patterns:
            if re.search(pattern, description_lower):
                if 'master' in pattern or 'phd' in pattern:
                    return "Master's/PhD preferred"
                else:
                    return "Bachelor's degree"
                    
        return "Not specified"
    
    def save_jobs_to_database(self, jobs: List[JobPosting]) -> int:
        """Save scraped jobs to database"""
        if not jobs:
            return 0
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        
        for job in jobs:
            try:
                # Insert or ignore company
                cursor.execute(
                    "INSERT OR IGNORE INTO companies (company_name) VALUES (?)",
                    (job.company,)
                )
                
                # Get company_id
                cursor.execute(
                    "SELECT company_id FROM companies WHERE company_name = ?",
                    (job.company,)
                )
                company_id = cursor.fetchone()[0]
                
                # Insert job (avoid duplicates based on company + role)
                cursor.execute("""
                INSERT OR IGNORE INTO job_requirements
                (company_id, role, required_skills, tools, experience, education, job_description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    company_id,
                    job.role,
                    job.required_skills,
                    job.tools,
                    job.experience,
                    job.education,
                    job.job_description
                ))
                
                if cursor.rowcount > 0:
                    saved_count += 1
                    
            except Exception as e:
                logger.error(f"Error saving job {job.company} - {job.role}: {e}")
                
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {saved_count} new jobs to database")
        return saved_count
    
    def run_full_scrape(self) -> Dict[str, int]:
        """Run a full scraping session across all sources"""
        logger.info("🚀 Starting real-time job scraping...")
        
        # Define search parameters
        tech_keywords = [
            'Software Engineer', 'Data Scientist', 'Machine Learning Engineer',
            'Frontend Developer', 'Backend Developer', 'Full Stack Developer',
            'DevOps Engineer', 'Product Manager', 'UI/UX Designer'
        ]
        
        locations = ['United States', 'Remote', 'New York', 'San Francisco', 'Seattle']
        
        all_jobs = []
        results = {}
        
        # Scrape from different sources
        try:
            # RemoteOK (free API)
            remote_jobs = self.scrape_github_jobs(tech_keywords, limit=100)
            all_jobs.extend(remote_jobs)
            results['RemoteOK'] = len(remote_jobs)
            logger.info(f"✅ Scraped {len(remote_jobs)} jobs from RemoteOK")
            
        except Exception as e:
            logger.error(f"❌ Error scraping RemoteOK: {e}")
            results['RemoteOK'] = 0
        
        # Add more sources as needed
        # results['Adzuna'] = len(adzuna_jobs)
        # results['Indeed'] = len(indeed_jobs)
        
        # Save to database
        saved_count = self.save_jobs_to_database(all_jobs)
        results['total_scraped'] = len(all_jobs)
        results['total_saved'] = saved_count
        
        logger.info(f"🎉 Scraping complete! Total: {len(all_jobs)} jobs, Saved: {saved_count} new jobs")
        
        return results

def main():
    """Main function to run the job scraper"""
    scraper = JobScraper()
    results = scraper.run_full_scrape()
    
    print("\n" + "="*50)
    print("📊 JOB SCRAPING RESULTS")
    print("="*50)
    
    for source, count in results.items():
        print(f"{source}: {count} jobs")
    
    print("="*50)
    print(f"✅ Successfully updated database with real-time job data!")

if __name__ == "__main__":
    main()