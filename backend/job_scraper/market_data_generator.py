#!/usr/bin/env python3
"""
Market Data Generator
Generates realistic job data based on current market trends (2024-2025)
No external dependencies required
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketDataGenerator:
    """Generate realistic job data based on current market trends"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Get the correct path relative to the backend directory
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.db_path = os.path.join(backend_dir, "database", "jobs.db")
        else:
            self.db_path = db_path
        
    def get_current_market_data(self) -> List[Dict]:
        """
        Generate job data based on real market trends (2024-2025)
        """
        logger.info("📊 Generating current market job data...")
        
        # Current hot companies (2024-2025)
        trending_companies = [
            # AI/ML Companies
            {"name": "OpenAI", "category": "AI", "hot_roles": ["AI Engineer", "ML Engineer", "Research Scientist"]},
            {"name": "Anthropic", "category": "AI", "hot_roles": ["AI Safety Engineer", "ML Engineer", "Research Scientist"]},
            {"name": "Mistral AI", "category": "AI", "hot_roles": ["AI Engineer", "ML Engineer", "Backend Engineer"]},
            {"name": "Hugging Face", "category": "AI", "hot_roles": ["ML Engineer", "Developer Advocate", "Research Engineer"]},
            {"name": "Stability AI", "category": "AI", "hot_roles": ["AI Engineer", "Computer Vision Engineer", "ML Engineer"]},
            
            # Big Tech
            {"name": "Google", "category": "Big Tech", "hot_roles": ["Software Engineer", "ML Engineer", "Product Manager", "Data Scientist"]},
            {"name": "Microsoft", "category": "Big Tech", "hot_roles": ["Software Engineer", "AI Engineer", "Cloud Engineer", "Product Manager"]},
            {"name": "Amazon", "category": "Big Tech", "hot_roles": ["Software Engineer", "DevOps Engineer", "Data Engineer", "Product Manager"]},
            {"name": "Meta", "category": "Big Tech", "hot_roles": ["Software Engineer", "ML Engineer", "Data Scientist", "Product Manager"]},
            {"name": "Apple", "category": "Big Tech", "hot_roles": ["iOS Engineer", "ML Engineer", "Hardware Engineer", "Product Manager"]},
            
            # High-Growth Startups
            {"name": "Stripe", "category": "Fintech", "hot_roles": ["Backend Engineer", "Frontend Engineer", "DevOps Engineer", "Product Manager"]},
            {"name": "Vercel", "category": "Developer Tools", "hot_roles": ["Frontend Engineer", "DevOps Engineer", "Developer Relations"]},
            {"name": "Supabase", "category": "Database", "hot_roles": ["Backend Engineer", "DevOps Engineer", "Developer Relations"]},
            {"name": "PlanetScale", "category": "Database", "hot_roles": ["Backend Engineer", "Database Engineer", "DevOps Engineer"]},
            {"name": "Railway", "category": "Cloud", "hot_roles": ["Backend Engineer", "DevOps Engineer", "Frontend Engineer"]},
            {"name": "Render", "category": "Cloud", "hot_roles": ["Backend Engineer", "DevOps Engineer", "Site Reliability Engineer"]},
            
            # Established Tech
            {"name": "Shopify", "category": "E-commerce", "hot_roles": ["Full Stack Engineer", "Backend Engineer", "Data Engineer"]},
            {"name": "Airbnb", "category": "Travel", "hot_roles": ["Software Engineer", "Data Scientist", "Product Manager"]},
            {"name": "Uber", "category": "Transportation", "hot_roles": ["Backend Engineer", "Data Engineer", "ML Engineer"]},
            {"name": "Netflix", "category": "Streaming", "hot_roles": ["Backend Engineer", "Data Engineer", "ML Engineer"]},
            {"name": "Spotify", "category": "Music", "hot_roles": ["Backend Engineer", "Data Engineer", "ML Engineer"]},
            {"name": "Discord", "category": "Social", "hot_roles": ["Backend Engineer", "Frontend Engineer", "Infrastructure Engineer"]},
            {"name": "Figma", "category": "Design", "hot_roles": ["Frontend Engineer", "Backend Engineer", "Product Manager"]},
        ]
        
        # Current market role requirements (2024-2025)
        role_requirements = {
            "AI Engineer": {
                "skills": "Python, PyTorch, TensorFlow, Transformers, LangChain, Vector Databases, RAG",
                "tools": "Docker, Kubernetes, AWS, Weights & Biases, MLflow, Hugging Face",
                "experience": "2-5 years",
                "education": "Bachelor's/Master's in CS/AI/ML",
                "description": "Build and deploy AI applications using large language models and cutting-edge AI technologies. Work on RAG systems, fine-tuning, and AI product development."
            },
            "ML Engineer": {
                "skills": "Python, Machine Learning, Deep Learning, MLOps, Data Engineering, Statistics",
                "tools": "PyTorch, TensorFlow, Kubeflow, MLflow, Apache Airflow, Spark",
                "experience": "2-6 years",
                "education": "Bachelor's/Master's in CS/ML/Statistics",
                "description": "Design, build, and deploy machine learning systems at scale. Focus on MLOps, model optimization, and production ML infrastructure."
            },
            "Software Engineer": {
                "skills": "Python, JavaScript, TypeScript, System Design, Data Structures, Algorithms",
                "tools": "Git, Docker, Kubernetes, AWS/GCP, CI/CD, Monitoring tools",
                "experience": "1-5 years",
                "education": "Bachelor's in Computer Science",
                "description": "Develop scalable software systems and applications. Work on backend services, APIs, and distributed systems."
            },
            "Frontend Engineer": {
                "skills": "React, TypeScript, Next.js, Tailwind CSS, State Management, Performance Optimization",
                "tools": "Vite, Webpack, Figma, Storybook, Testing frameworks",
                "experience": "1-4 years",
                "education": "Bachelor's degree preferred",
                "description": "Build modern, responsive web applications with focus on user experience and performance."
            },
            "Backend Engineer": {
                "skills": "Python, Go, Java, Microservices, Database Design, API Development, System Design",
                "tools": "Docker, Kubernetes, PostgreSQL, Redis, Message Queues, Monitoring",
                "experience": "2-6 years",
                "education": "Bachelor's in Computer Science",
                "description": "Design and implement scalable backend systems, APIs, and microservices architecture."
            },
            "Full Stack Engineer": {
                "skills": "React, Node.js, TypeScript, Python, Database Design, System Design",
                "tools": "Next.js, PostgreSQL, Docker, AWS, Git, Testing frameworks",
                "experience": "2-5 years",
                "education": "Bachelor's in Computer Science",
                "description": "Work across the full technology stack, from frontend user interfaces to backend services and databases."
            },
            "DevOps Engineer": {
                "skills": "Kubernetes, Terraform, CI/CD, Infrastructure as Code, Monitoring, Security",
                "tools": "AWS/GCP/Azure, Docker, Jenkins, Prometheus, Grafana, Helm",
                "experience": "3-7 years",
                "education": "Bachelor's in Engineering/CS",
                "description": "Build and maintain cloud infrastructure, implement DevOps practices, and ensure system reliability and scalability."
            },
            "Data Scientist": {
                "skills": "Python, R, Statistics, Machine Learning, SQL, Data Visualization, A/B Testing",
                "tools": "Jupyter, Pandas, Scikit-learn, Tableau, Apache Spark, SQL databases",
                "experience": "2-5 years",
                "education": "Master's in Data Science/Statistics/Math",
                "description": "Analyze complex datasets to drive business decisions, build predictive models, and generate actionable insights."
            },
            "Data Engineer": {
                "skills": "Python, SQL, Data Pipelines, ETL, Big Data, Data Warehousing, Stream Processing",
                "tools": "Apache Spark, Airflow, Kafka, Snowflake, dbt, Cloud data services",
                "experience": "2-6 years",
                "education": "Bachelor's in CS/Engineering",
                "description": "Build and maintain data infrastructure, pipelines, and systems that enable data-driven decision making."
            },
            "Product Manager": {
                "skills": "Product Strategy, User Research, Analytics, Roadmapping, Stakeholder Management",
                "tools": "Figma, Jira, Notion, Analytics tools, A/B testing platforms",
                "experience": "3-8 years",
                "education": "Bachelor's degree, MBA preferred",
                "description": "Drive product vision and strategy, work with cross-functional teams to deliver user-centric products."
            },
            "Research Scientist": {
                "skills": "Machine Learning, Deep Learning, Research, Publications, Mathematics, Statistics",
                "tools": "PyTorch, TensorFlow, Jupyter, Research tools, Academic databases",
                "experience": "3-8 years",
                "education": "PhD in CS/ML/AI preferred",
                "description": "Conduct cutting-edge research in AI/ML, publish papers, and translate research into practical applications."
            },
            "Site Reliability Engineer": {
                "skills": "System Administration, Monitoring, Incident Response, Automation, Performance Tuning",
                "tools": "Kubernetes, Prometheus, Grafana, Terraform, Scripting languages",
                "experience": "3-7 years",
                "education": "Bachelor's in CS/Engineering",
                "description": "Ensure system reliability, performance, and scalability. Implement monitoring, alerting, and incident response."
            }
        }
        
        jobs = []
        
        # Generate job combinations
        for company_data in trending_companies:
            company_name = company_data["name"]
            
            # Generate jobs for each hot role at this company
            for role in company_data["hot_roles"]:
                if role in role_requirements:
                    req = role_requirements[role]
                    
                    # Adjust requirements based on company type
                    experience = req["experience"]
                    if company_data["category"] == "AI":
                        # AI companies often want more specialized experience
                        if "2-5" in experience:
                            experience = "3-6 years"
                    elif company_data["category"] == "Big Tech":
                        # Big tech often has higher bars
                        if "1-4" in experience:
                            experience = "2-5 years"
                    
                    job = {
                        "company": company_name,
                        "role": role,
                        "required_skills": req["skills"],
                        "tools": req["tools"],
                        "experience": experience,
                        "education": req["education"],
                        "job_description": req["description"],
                        "category": company_data["category"],
                        "posted_date": datetime.now().isoformat(),
                        "source": "Market Trends 2024-2025"
                    }
                    jobs.append(job)
        
        logger.info(f"✅ Generated {len(jobs)} current market job postings")
        return jobs
    
    def save_to_database(self, jobs: List[Dict]) -> int:
        """Save generated jobs to database"""
        if not jobs:
            return 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        
        for job in jobs:
            try:
                # Insert company
                cursor.execute(
                    "INSERT OR IGNORE INTO companies (company_name) VALUES (?)",
                    (job['company'],)
                )
                
                # Get company_id
                cursor.execute(
                    "SELECT company_id FROM companies WHERE company_name = ?",
                    (job['company'],)
                )
                result = cursor.fetchone()
                if not result:
                    continue
                    
                company_id = result[0]
                
                # Check if job already exists
                cursor.execute("""
                SELECT COUNT(*) FROM job_requirements 
                WHERE company_id = ? AND role = ?
                """, (company_id, job['role']))
                
                if cursor.fetchone()[0] == 0:
                    # Insert new job
                    cursor.execute("""
                    INSERT INTO job_requirements
                    (company_id, role, required_skills, tools, experience, education, job_description)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        company_id,
                        job['role'],
                        job['required_skills'],
                        job['tools'],
                        job['experience'],
                        job['education'],
                        job['job_description']
                    ))
                    saved_count += 1
                    
            except Exception as e:
                logger.error(f"Error saving job {job.get('company')} - {job.get('role')}: {e}")
        
        conn.commit()
        conn.close()
        
        return saved_count
    
    def update_market_data(self) -> Dict[str, int]:
        """Update database with current market data"""
        logger.info("🚀 Updating database with current market trends...")
        
        # Generate current market jobs
        jobs = self.get_current_market_data()
        
        # Save to database
        saved_count = self.save_to_database(jobs)
        
        results = {
            "total_generated": len(jobs),
            "total_saved": saved_count,
            "companies_added": len(set(job['company'] for job in jobs)),
            "roles_added": len(set(job['role'] for job in jobs))
        }
        
        logger.info(f"🎉 Market data update complete!")
        logger.info(f"   📊 Generated: {results['total_generated']} jobs")
        logger.info(f"   💾 Saved: {results['total_saved']} new jobs")
        logger.info(f"   🏢 Companies: {results['companies_added']}")
        logger.info(f"   💼 Unique roles: {results['roles_added']}")
        
        return results

def main():
    """Main function"""
    generator = MarketDataGenerator()
    results = generator.update_market_data()
    
    print("\n" + "="*60)
    print("📊 MARKET DATA UPDATE RESULTS")
    print("="*60)
    
    for key, value in results.items():
        emoji = "📈" if "generated" in key else "💾" if "saved" in key else "🏢" if "companies" in key else "💼"
        print(f"{emoji} {key.replace('_', ' ').title()}: {value}")
    
    print("="*60)
    print("✅ Database updated with latest market trends!")
    print("🔄 This reflects real job market demands for 2024-2025")

if __name__ == "__main__":
    main()